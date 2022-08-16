from django.contrib import admin

from .models import (LoanProduct, LoanConsultation, LoanApplication, LoanDocument, SocialAnalysis, Loan,
                     KIBAnalysis, TundukAnalysis, LoanApllicationConfirmEmployees, LoanApplicationConfirmHistory,
                     LoanInitialPaymentValue, LoanLimitAmount, LoanLimitAmountHistory, LoanInfo)

# Register your models here.
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_registered', 'client', 'is_accept', 'is_processing', 'give_out_status', 'loan_product', 'loan_product_percent', 'funding_amount',
                    'funding_period', 'created_date')

    search_fields = ('__str__',)
    list_filter = ('is_registered', 'is_accept', 'give_out_status', 'is_processing', 'loan_product', 'created_date')
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
    

class LoanApplicationConfirmHistoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_confirm', 'created_date')

    search_fields = ('loan_application', 'employee')
    list_filter = ('loan_application', 'employee', 'is_confirm')
    date_hierarchy = 'created_date'
    

class LoanApllicationConfirmEmployeesAdmin(admin.ModelAdmin):
    list_display = ('employee', 'is_active', 'created_date', 'updated_date')

    search_fields = ('employee',)
    list_filter = ('is_active',)
    date_hierarchy = 'created_date'


class KIBAnalysisAdmin(admin.ModelAdmin):
    list_display = ('loan_application', 'created_date')

    search_fields = ('loan_application',)
    list_filter = ('created_date',)
    date_hierarchy = 'created_date'
    
    
class TundukAnalysisAdmin(admin.ModelAdmin):
    list_display = ('loan_application', 'created_date')

    search_fields = ('loan_application',)
    list_filter = ('created_date',)
    date_hierarchy = 'created_date'
    

class SocialAnalysisAdmin(admin.ModelAdmin):
    list_display = ('loan_application', 'is_match', 'client_loans_history', 'is_positive', 'created_date')

    list_filter = ('created_date', 'profession_relevance', 'is_match', 'client_loans_history', 'own_house_address', 'has_a_car', 'сlient_behavior', 'is_swear', 'is_sharia_type_of_activity', 'is_positive')
    date_hierarchy = 'created_date'


class LoanAdmin(admin.ModelAdmin):
    list_display = ('balance_account', 'loan_application', 'deposit_account', 'classification', 'classification_percent',
                    'urgent_principal_debt', 'overdue_principal_debt', 'overdue_days_quantity', 'total_overdue_days_quantity', 
                    'is_overdue', 'accrual_status', 'accrual_status_date', 'created_date')

    search_fields = ('loan_application',)
    list_filter = ('classification', 'classification_percent', 'is_overdue', 'created_date',)
    date_hierarchy = 'created_date'
    

class LoanInitialPaymentValueAdmin(admin.ModelAdmin):
    list_display = ('total_cost', 'get_percent', 'updated_date')

    list_filter = ('created_date',)
    date_hierarchy = 'created_date'
    

class LoanLimitAmountAdmin(admin.ModelAdmin):
    list_display = ('position', 'limit', 'updated_date')

    list_filter = ('created_date',)
    date_hierarchy = 'created_date'
    

class LoanLimitAmountHistoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'limit', 'is_current', 'start_date', 'end_date', 'updated_date')

    list_filter = ('created_date',)
    date_hierarchy = 'created_date'


class LoanInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_date', 'updated_date')

    list_filter = ('created_date',)
    date_hierarchy = 'created_date'
    

admin.site.register(LoanProduct, LoanProductAdmin)
admin.site.register(LoanConsultation, LoanConsultationAdmin)
admin.site.register(LoanApplication, LoanApplicationAdmin)
admin.site.register(LoanDocument, LoanDocumentAdmin)
admin.site.register(KIBAnalysis, KIBAnalysisAdmin)
admin.site.register(TundukAnalysis, TundukAnalysisAdmin)
admin.site.register(SocialAnalysis, SocialAnalysisAdmin)
admin.site.register(LoanApplicationConfirmHistory, LoanApplicationConfirmHistoryAdmin)
admin.site.register(LoanApllicationConfirmEmployees, LoanApllicationConfirmEmployeesAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(LoanInitialPaymentValue, LoanInitialPaymentValueAdmin)
admin.site.register(LoanLimitAmount, LoanLimitAmountAdmin)
admin.site.register(LoanLimitAmountHistory, LoanLimitAmountHistoryAdmin)
admin.site.register(LoanInfo, LoanInfoAdmin)
