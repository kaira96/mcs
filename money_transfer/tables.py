from django.utils.translation import gettext_lazy as _
from django.contrib.humanize.templatetags.humanize import intcomma

from django_tables2_column_shifter.tables import ColumnShiftTableBootstrap4
from django_tables2.utils import A
from django_tables2.columns import LinkColumn 

from .models import MoneyTransfer



class MoneyTransferTable(ColumnShiftTableBootstrap4):
    
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.table_pagination = True
        
    id = LinkColumn(
        # custom loan url   
        "money-transfer-detail", 
        args=[A("id")],
        verbose_name = _(' № '),
        )
    
    def get_column_default_show(self):
        self.column_default_show = ('id', 'trade_partner', 'loan', 'transfer_amount', 'is_transfered', 'created_date')
        return super().get_column_default_show()
    
    def render_transfer_amount_debt(self, value):
        return intcomma(value)

    class Meta:
        model = MoneyTransfer
        template_name = 'django_tables2/bootstrap.html'
        fields = ('id', 'trade_partner', 'loan', 'employee', 'branch',
                  'transfer_amount', 'is_transfered', 'created_date')
        

class MoneyTransferedTable(ColumnShiftTableBootstrap4):
    
    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.table_pagination = True
        self.base_columns['id'].verbose_name = '№'
        self.base_columns['updated_date'].verbose_name = _('Время перевода средств ТО')
    
    def get_column_default_show(self):
        self.column_default_show = ('id', 'trade_partner', 'loan', 'transfer_amount', 'is_transfered', 'updated_date')
        return super().get_column_default_show()
    
    def render_transfer_amount_debt(self, value):
        return intcomma(value)

    class Meta:
        model = MoneyTransfer
        template_name = 'django_tables2/bootstrap.html'
        fields = ('id', 'trade_partner', 'loan', 'employee', 'branch',
                  'transfer_amount', 'is_transfered', 'updated_date')
