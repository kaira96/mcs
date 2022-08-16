from django.contrib import admin

from .models import Deposit


# Register your models here.
class DepositAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'balance_account', 'client', 'current_balance', 'date_of_last_deposit')
    list_filter = ('created_date', 'branch', 'employee', 'is_active', 'is_blocked')
    search_fields = ('client',)
    date_hierarchy = 'created_date'
    
    def save_model(self, request, obj, form, change):
        obj.save(request=request)


admin.site.register(Deposit, DepositAdmin)
