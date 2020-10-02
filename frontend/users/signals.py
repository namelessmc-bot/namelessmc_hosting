# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.dispatch import receiver
from .models import Account

# def create_account(sender, instance, created, **kwargs):
def create_account(_, instance, created, **__):
    if created:
        Account.objects.create(user=instance)


def save_account(_, instance, __, **___):
    instance.account.save()
