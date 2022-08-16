from django.contrib import admin
from .models import (
    Client, ClientSalary, Spouse,
    Guarantor, Passport, Job,
    Dependent, ClientSpend, ClientCommercial
)


# Register your models here.
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'gender', 'residence_address',
                    'phone_number', 'date_of_birth',
                    'registration_address', 'is_married',
                    'is_criminal_record', 'education_status')

    search_fields = ('first_name', 'last_name', 'middle_name')
    list_filter = ('gender', 'education_status', 'is_married', 'is_criminal_record')
    date_hierarchy = 'created_date'
    

class SpouseAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'client', 'is_guarantor',
                    'passport', 'residence_address', 'phone_number')

    search_fields = ('first_name', 'last_name', 'middle_name')
    list_filter = ('gender', 'education_status', 'is_guarantor')
    date_hierarchy = 'created_date'


class GurantorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'client',
                    'passport', 'residence_address', 'phone_number')

    search_fields = ('first_name', 'last_name', 'middle_name')
    list_filter = ('gender', 'education_status')
    date_hierarchy = 'created_date'
    
    
class PassportAdmin(admin.ModelAdmin):
    list_display = ('series_type', 'series', 'pin',
                    'date_of_issue')

    search_fields = ('series', 'pin')
    list_filter = ('series_type',)
    date_hierarchy = 'created_date'
    

class ClientSalaryAdmin(admin.ModelAdmin):
    list_display = ('salary', 'client',
                    'start_date', 'end_date', 'is_current')

    search_fields = ('client',)
    list_filter = ('is_current',)
    date_hierarchy = 'created_date'
    
    

class JobAdmin(admin.ModelAdmin):
    list_display = ('name', 'client',
                    'position', 'date_of_employment', 'company_definition')

    search_fields = ('name', 'position', 'client', 'company_definition')
    list_filter = ('name', 'company_definition')
    date_hierarchy = 'created_date'
    
     
class DependentAdmin(admin.ModelAdmin):
    list_display = ('client', 'children_under_18', 
                    'another_dependents')

    search_fields = ('client',)
    date_hierarchy = 'created_date'
    
    
class ClientSpendAdmin(admin.ModelAdmin):
    list_display = ('title', 'per_month_amount', 'is_active')

    search_fields = ('title',)
    date_hierarchy = 'created_date'
        
    

admin.site.register(Client, ClientAdmin)
admin.site.register(Spouse, SpouseAdmin)
admin.site.register(Guarantor, GurantorAdmin)
admin.site.register(Passport, PassportAdmin)
admin.site.register(ClientSalary, ClientSalaryAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Dependent, DependentAdmin)
admin.site.register(ClientSpend, ClientSpendAdmin)
admin.site.register(ClientCommercial)
