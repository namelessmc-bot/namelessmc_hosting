from django.contrib import admin
from .models import Account, Website, Job, Transaction, Voucher


class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'domain', 'use_https', 'www', 'version', 'date_created', 'down_since')


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')


class JobAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'priority', 'content', 'done', 'running')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'product', 'target_email', 'payer_email', 'currency', 'target_user', 'success')


class VoucherAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'amount')


admin.site.register(Website, WebsiteAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Voucher, VoucherAdmin)
