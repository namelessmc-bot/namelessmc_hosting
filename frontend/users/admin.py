from django.contrib import admin
from .models import Account, Website, Job, Transaction, Voucher

admin.site.register(Website)
admin.site.register(Account)
admin.site.register(Job)
admin.site.register(Transaction)
admin.site.register(Voucher)
