from django.contrib import admin
from .models import Account, Website, Job, Transaction

admin.site.register(Website)
admin.site.register(Account)
admin.site.register(Job)
admin.site.register(Transaction)
