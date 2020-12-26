from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from .utils import pass_gen

def validate_domain(value):
    # TODO there has to be a better way
    allowed_domain_chars = ['_', '-', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',\
                            'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',\
                            's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2',\
                            '3', '4', '5', '6', '7', '8', '9', '0', '.']
    for char in value:
        if char not in allowed_domain_chars:
            raise ValidationError("Invalid domain", params={'value': value})

    if 'rs-sys.nl' in value \
        or value in ['namedhosting.com', 'site.namedhosting.com', \
                        'www.namedhosting.com']:
        raise ValidationError("Invalid domain", params={'value': value})

    if 'www.' in value:
        raise ValidationError("Don't include www. in your domain", params={'value': value})

    if not '.' in value:
        raise ValidationError("Invalid domain", params={'value': value})


class Website(models.Model):
    domain = models.CharField(max_length=100, unique=True, validators=[validate_domain])
    use_https = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    db_password = models.CharField(max_length=50, default=pass_gen)
    files_password = models.CharField(max_length=50, default=pass_gen)
    versions_choices = [
        ('v2-pr7', 'v2-pr7 (previous stable)'),
        ('v2-pr8', 'v2-pr8 (current stable)'),
        ('v2-pr9dev', 'v2-pr9 development - TESTING ONLY'),
        ('v2-pr9dev-php8', 'v2-pr9 development on PHP 8 - TESTING ONLY')
    ]
    version = models.CharField(max_length=20, default='v2-pr8', choices=versions_choices)
    webserver_ip = models.CharField(max_length=20, default=None, null=True)
    www = models.BooleanField(default=False, verbose_name='Enable www.')

    def __str__(self):
        return self.domain


    def get_absolute_url(self):
        return reverse("website-detail", kwargs={"pk": self.pk})


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credit = models.IntegerField(default=30)

    def __str__(self):
        return f'{self.user.username} - {self.credit} Account'


class Job(models.Model):
    class Meta:
        db_table = 'jobs'

    CREATE_WEBSITE = 0 # Create website dataset and containers
    UPDATE_WEBSITE = 1 # Update domain and/or database password
    RESET_WEBSITE = 2
    RESERVED = 3
    DELETE_WEBSITE = 4 # Delete website and all data

    JOB_TYPES = [
        (CREATE_WEBSITE, 'Create website'),
        (UPDATE_WEBSITE, 'Update website'),
        (RESET_WEBSITE, 'Reset website'),
        (RESERVED, 'nothing'),
        (DELETE_WEBSITE, 'Delete website'),
    ]

    CRITICAL = 4
    HIGH = 3
    NORMAL = 2
    LOW = 1
    BACKGROUND = 0

    PRIORITIES = [
        (CRITICAL, 'Critical'),
        (HIGH, 'High'),
        (NORMAL, 'Normal'),
        (LOW, 'Low'),
        (BACKGROUND, 'Background'),
    ]

    type = models.IntegerField(choices=JOB_TYPES)
    priority = models.IntegerField(choices=PRIORITIES)
    content = models.CharField(max_length=200, null=True)
    done = models.BooleanField(default=False)
    running = models.BooleanField(default=False)


class Transaction(models.Model):
    price = models.IntegerField(null=True)
    product = models.CharField(max_length=30, null=True)
    target_email = models.CharField(max_length=100, null=True)
    payer_email = models.CharField(max_length=200, null=True)
    currency = models.CharField(max_length=10, null=True)
    target_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    success = models.BooleanField()


class Voucher(models.Model):
    code = models.CharField(max_length=50, default=pass_gen, unique=True)
    amount = models.IntegerField(default=30)

    def __str__(self):
        return f'{self.amount} credits voucher {self.code}'
