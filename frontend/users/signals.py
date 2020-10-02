from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Account, Website, Job

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
        Job.objects.create(type=Job.CREATE_WEBSITE, priority=Job.NORMAL, content=instance.id)
    else:
        Job.objects.create(type=Job.UPDATE_WEBSITE, priority=Job.HIGH, content=instance.pk)
