from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
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
            raise ValidationError(_('Invalid domain'), params={'value': value})

    if 'rs-sys.nl' in value \
        or value in ['namedhosting.com', 'site.namedhosting.com', \
                        'www.namedhosting.com']:
        raise ValidationError(_('Invalid domain'), params={'value': value})

    if 'www.' in value:
        raise ValidationError(_("Don't include www. in your domain"), params={'value': value})

    if not '.' in value:
        raise ValidationError(_('Invalid domain'), params={'value': value})


class Website(models.Model):
    domain = models.CharField(max_length=100, unique=True, validators=[validate_domain], verbose_name=_('Domain'))
    use_https = models.BooleanField(default=False, verbose_name=_('Use HTTPS?'))
    date_created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, verbose_name=_('Website name'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    db_password = models.CharField(max_length=50, default=pass_gen)
    files_password = models.CharField(max_length=50, default=pass_gen)
    versions_choices = [
        ('v2-pr7', _('v2 pre release 7 (old)')),
        ('v2-pr8', _('v2 pre release 8 (previous)')),
        ('v2-pr9', _('v2 pre release 9 (current)')),
        ('v2-pr9-php8', _('v2 pre release 9 on PHP 8 - TESTING ONLY')),
        ('dev', _('Development - TESTING ONLY')),
        ('dev-php8', _('Development on PHP 8 - TESTING ONLY'))
    ]
    version = models.CharField(max_length=20, default='v2-pr9', choices=versions_choices, verbose_name=_('Version'))
    webserver_ip = models.CharField(max_length=20, default=None, null=True, blank=True)
    www = models.BooleanField(default=False, verbose_name=_('Enable www.'))
    down_since = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return f'{self.name} - {self.domain}'


    def get_absolute_url(self):
        return reverse("website-detail", kwargs={"pk": self.pk})


    class Meta:
        ordering = ['name']


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'


class Job(models.Model):
    class Meta:
        db_table = 'jobs'

    CREATE_WEBSITE = 0 # Create website dataset and containers
    UPDATE_WEBSITE = 1 # Update domain and/or database password
    RESET_WEBSITE = 2
    RENEW_CERT = 3
    DELETE_WEBSITE = 4 # Delete website and all data
    START_WEBSITE = 5
    PING_WEBSITE = 6

    JOB_TYPES = [
        (CREATE_WEBSITE, 'Create website'),
        (UPDATE_WEBSITE, 'Update website'),
        (RESET_WEBSITE, 'Reset website'),
        (RENEW_CERT, 'Renew certificate'),
        (DELETE_WEBSITE, 'Delete website'),
        (START_WEBSITE, 'Start website'),
        (PING_WEBSITE, 'Ping website'),
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
    priority = models.IntegerField(choices=PRIORITIES, default=NORMAL)
    content = models.CharField(max_length=200, null=True, blank=True)
    done = models.BooleanField(default=False)
    running = models.BooleanField(default=False)


class Transaction(models.Model):
    price = models.IntegerField(null=True, blank=True)
    product = models.CharField(max_length=30, null=True, blank=True)
    target_email = models.CharField(max_length=100, null=True, blank=True)
    payer_email = models.CharField(max_length=200, null=True, blank=True)
    currency = models.CharField(max_length=10, null=True, blank=True)
    target_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    success = models.BooleanField()


class Voucher(models.Model):
    code = models.CharField(max_length=50, default=pass_gen, unique=True)
    amount = models.IntegerField(default=30)

    def __str__(self):
        return f'{self.amount} credits voucher {self.code}'
