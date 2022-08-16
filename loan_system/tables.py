from django.utils.translation import gettext_lazy as _
from django.contrib.humanize.templatetags.humanize import intcomma

from django_tables2_column_shifter.tables import ColumnShiftTableBootstrap4
from django_tables2.utils import A
from django_tables2.columns import LinkColumn 

from loan_system.models import LoanConsultation, LoanApplication, Loan


class LoanConsultationTable(ColumnShiftTableBootstrap4):
    
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.table_pagination = True
        
    id = LinkColumn(
        # custom loan url 
        "loan-consultation-detail", 
        args=[A("id")],
        verbose_name = _(' № '),
        )
    
    def get_column_default_show(self):
        self.column_default_show = ('id', 'loan_product', 'funding_amount', 'funding_period', 'created_date')
        return super().get_column_default_show()

    class Meta:
        model = LoanConsultation
        template_name = 'django_tables2/bootstrap.html'
        fields = ('id', 'loan_product', 'funding_amount', 'funding_period', 'first_instalment', 'is_re_financing', 'is_employer', 'is_gurantor', 'created_date') 
    

class LoanApplicationTable(ColumnShiftTableBootstrap4):
    
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.table_pagination = True
        
    id = LinkColumn(
        # custom loan url   
        "loan-application-detail", 
        args=[A("id")],
        verbose_name = _(' № '),
        )
    
    def get_column_default_show(self):
        self.column_default_show = ('id', 'is_accept', 'give_out_status', 'employee', 'loan_product', 'funding_amount', 'funding_period', 'created_date')
        return super().get_column_default_show()
    
    def render_funding_amount(self, value):
        return intcomma(value)

    class Meta:
        model = LoanApplication
        template_name = 'django_tables2/bootstrap.html'
        fields = ('id', 'is_registered', 'is_accept', 'is_processing', 'give_out_status', 'client', 'employee', 'loan_product', 'funding_amount', 'funding_period', 'first_instalment', 'created_date') 


class LoanApplicationConfirmTable(LoanApplicationTable):
    id = LinkColumn(
        # custom loan url   
        "loan-application-confirm-detail", 
        args=[A("id")],
        verbose_name = _(' № '),
        )


class LoanTable(ColumnShiftTableBootstrap4):
    
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.table_pagination = True
        
    id = LinkColumn(
        # custom loan url   
        "loan-detail", 
        args=[A("id")],
        verbose_name = _(' № '),
        )
    
    def get_column_default_show(self):
        self.column_default_show = ('id', 'loan_application', 'is_overdue', 'classification', 'overdue_days_quantity', 'urgent_principal_debt', 'overdue_principal_debt', 'updated_date')
        return super().get_column_default_show()
    
    def render_urgent_principal_debt(self, value):
        return intcomma(value)
    
    def render_overdue_principal_debt(self, value):
        return intcomma(value)

    class Meta:
        model = Loan
        template_name = 'django_tables2/bootstrap.html'
        fields = ('id', 'deposit_account', 'balance_account', 'loan_application', 
                  'classification', 'classification_percent', 'overdue_days_quantity',
                  'total_overdue_days_quantity', 'is_overdue', 'accrual_status', 'accrual_status_date', 'created_date',
                  'urgent_principal_debt', 'overdue_principal_debt', 'updated_date')
