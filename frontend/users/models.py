from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Website(models.Model):
    domain = models.CharField(max_length=100)
    use_https = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    db_password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs): # pylint: disable=signature-differs
        super().save(*args, **kwargs)
        # TODO update docker dingen

    def get_absolute_url(self):
        return reverse("website-detail", kwargs={"pk": self.pk})


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credit = models.IntegerField(default=30)

    def __str__(self):
        return f'{self.user.username} Account'
