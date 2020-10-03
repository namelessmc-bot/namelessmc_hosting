from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from .utils import pass_gen

def validate_domain(value):
    # TODO there has to be a better way
    allowed_domain_chars = ['_','-','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0','.']
    for char in value:
        if char not in allowed_domain_chars:
            raise ValidationError("Invalid domain", params={'value': value})

    if 'rs-sys.nl' in value:
        raise ValidationError("Invalid domain", params={'value': value})

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

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse("website-detail", kwargs={"pk": self.pk})


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credit = models.IntegerField(default=30)

    def __str__(self):
        return f'{self.user.username} Account'


class Job(models.Model):
    class Meta:
        db_table = 'jobs'

    CREATE_WEBSITE = 0 # Create website dataset and containers
    UPDATE_WEBSITE = 1 # Update domain and/or database password
    RESET_DATABASE = 2 # Stop database container, delete files, start database container
    RESET_WEB = 3 # Delete all files in web/ directory and restart php container to re-download website
    DELETE_WEBSITE = 4 # Delete website and all data
    RECREATE_WEBSITE_CONTAINERS = 5 # Recreate docker containers for this website

    JOB_TYPES = [
        (CREATE_WEBSITE, 'Create website'),
        (UPDATE_WEBSITE, 'Update website'),
        (RESET_DATABASE, 'Reset database'),
        (RESET_WEB, 'Reset web'),
        (DELETE_WEBSITE, 'Delete website'),
        (RECREATE_WEBSITE_CONTAINERS, 'Recreate website containers'),
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
