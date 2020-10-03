from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Account, Website, Job
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
        Job.objects.create(type=Job.CREATE_WEBSITE, priority=Job.NORMAL, content=instance.id)
    else:
        Job.objects.create(type=Job.UPDATE_WEBSITE, priority=Job.HIGH, content=instance.pk)


@receiver(pre_delete, sender=Website)
def delete_website(sender, instance, using, **_kwargs): # pylint: disable=unused-argument
    content = f'{instance.id}_{instance.domain}'
    Job.objects.create(type=Job.DELETE_WEBSITE, priority=Job.LOW, content=content)
