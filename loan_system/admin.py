from django.contrib import admin

from .models import LoanProduct, LoanConsultation, LoanApplication, LoanDocument

# Register your models here.
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'client', 'acceptance_status', 'loan_product', 'loan_product_percent', 'funding_amount',
                    'funding_period', 'created_date')

    search_fields = ('__str__',)
    list_filter = ('acceptance_status', 'loan_product', 'created_date')
    date_hierarchy = 'created_date'
    

class LoanConsultationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'loan_product', 'loan_product_percent', 'funding_amount',
                    'funding_period', 'created_date')

    search_fields = ('__str__',)
    list_filter = ('loan_product', 'created_date')
    date_hierarchy = 'created_date'


class LoanProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_percent', 'is_active',
                    'start_date', 'end_date', 'created_date')

    search_fields = ('name',)
    list_filter = ('is_active',)
    date_hierarchy = 'created_date'
    
    
class LoanDocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'loan_product', 'is_active',
                    'start_date', 'end_date', 'created_date')

    search_fields = ('name',)
    list_filter = ('is_active',)
    date_hierarchy = 'created_date'



admin.site.register(LoanProduct, LoanProductAdmin)
admin.site.register(LoanConsultation, LoanConsultationAdmin)
admin.site.register(LoanApplication,    LoanApplicationAdmin)
admin.site.register(LoanDocument, LoanDocumentAdmin)