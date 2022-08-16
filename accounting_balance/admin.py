from django.contrib import admin
from django.shortcuts import get_object_or_404

from .models import Account, Transaction, Balance, AccountTransactionTemplate

from employee_account.models import Employee


# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'created_date')
    search_fields = ('number',)
    date_hierarchy = 'created_date'


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('account', 'debit_amount', 'credit_amount', 'created_date')
    list_filter = ('created_date', 'branch', 'employee')
    search_fields = ('account',)
    date_hierarchy = 'created_date'


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'amount', 'description')
    list_filter = ('created_date', 'branch', 'employee')
    search_fields = ('debit', 'credit')
    date_hierarchy = 'created_date'
    exclude = ('unique_code', 'ip_address', 'branch', 'employee')
    
    def save_model(self, request, obj, form, change):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = request.META.get('REMOTE_ADDR')

        obj.ip_address = ipaddress
        obj.employee = get_object_or_404(Employee, pk=request.user.id)
        obj.branch = obj.employee.office_branch
        obj.save()


class AccountTransactionTemplateAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'from_account', 'to_account', 'created_date')
    list_filter = ('created_date',)
    search_fields = ('__str__',)
    date_hierarchy = 'created_date'
    

admin.site.register(Account, AccountAdmin)
admin.site.register(Balance, BalanceAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(AccountTransactionTemplate, AccountTransactionTemplateAdmin)