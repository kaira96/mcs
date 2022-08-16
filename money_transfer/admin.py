from django.contrib import admin

from .models import MoneyTransfer

# Register your models here.
class MoneyTransferAdmin(admin.ModelAdmin):
    list_display = ('loan', 'transfer_amount', 'branch', 'employee', 'trade_partner', 'is_transfered', 'created_date')

    search_fields = ('loan', 'trade_partner__name', 'employee', 'branch'), 
    list_filter = ('is_transfered', 'trade_partner', 'employee', 'branch', 'created_date')
    date_hierarchy = 'created_date'

admin.site.register(MoneyTransfer, MoneyTransferAdmin)
