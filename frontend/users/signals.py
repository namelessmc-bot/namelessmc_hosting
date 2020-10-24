from django.db.models.signals import post_save, pre_delete
from django.db.models import F
from django.contrib.auth.models import User
from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from .models import Account, Website, Job, Transaction
from .utils import pass_gen

@receiver(post_save, sender=User)
def create_account(sender, instance, created, **_kwargs): # pylint: disable=unused-argument
    if created:
        Account.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_account(sender, instance, **_kwargs): # pylint: disable=unused-argument
    instance.account.save()


@receiver(post_save, sender=Website)
def save_website(sender, instance, created, **_kwargs): # pylint: disable=unused-argument
    if created:
        # Hack to set passwords without saving the objects (which would cause another job to be created)
        Website.objects.filter(id=instance.id).update(db_password=pass_gen(), files_password=pass_gen())
        Job.objects.create(type=Job.CREATE_WEBSITE, priority=Job.HIGH, content=instance.id)
    else:
        if Job.objects.filter(type=Job.UPDATE_WEBSITE, content=instance.pk, done=False, running=False).exists():
            print('Skipped creating job to prevent duplicates')
        else:
            Job.objects.create(type=Job.UPDATE_WEBSITE, priority=Job.NORMAL, content=instance.pk)


@receiver(pre_delete, sender=Website)
def delete_website(sender, instance, using, **_kwargs): # pylint: disable=unused-argument
    content = f'{instance.id}_{instance.domain}'
    Job.objects.filter(content=content).delete()
    Job.objects.create(type=Job.DELETE_WEBSITE, priority=Job.LOW, content=content)


def paypal_money_received(sender, **_kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        target_email = ipn_obj.receiver_email
        if target_email != "rs.systems@derkad.es":
            Transaction.objects.create(success=False, target_email=target_email)
            return

        # ALSO: for the same reason, check the amount received, `custom` etc.

        product = ipn_obj.item_number
        if product == "credits_30":
            expected_price = '5.0'
            credits_to_add = 30
        elif product == "credits_100":
            expected_price = '10.00'
            credits_to_add = 100
        else:
            Transaction.objects.create(success=False, target_email=target_email,
                                       product=product)
            return

        paid_price = ipn_obj.mc_gross
        if paid_price != expected_price:
            Transaction.objects.create(success=False, target_email=target_email,
                                       product=product, price=paid_price)

        paid_currency = ipn_obj.mc_currency
        if paid_currency != 'USD':
            Transaction.objects.create(success=False, target_email=target_email,
                                       product=product, price=paid_price,
                                       currency=paid_currency)
            return

        target_user = ipn_obj.custom
        user = User.objects.filter(pk=target_user)
        if user:
            Account.objects.filter(user=user).update(credit=F('credit') + credits_to_add)
            Transaction.objects.create(success=True, target_email=target_email,
                                       product=product, price=paid_price,
                                       currency=paid_currency, user=user)
        else:
            Transaction.objects.create(success=False, target_email=target_email,
                                       product=product, price=paid_price,
                                       currency=paid_currency)
    else:
        Transaction.objects.create(success=False)
        return


valid_ipn_received.connect(paypal_money_received)
