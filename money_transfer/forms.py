from django import forms
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Field

from .models import MoneyTransfer


class MoneyTransferDetailForm(forms.ModelForm):
    
    trade_partner = forms.CharField(label=_('Торговая организация'))
    loan = forms.CharField(label=_('Кредит'))
    employee = forms.CharField(label=_('Сотрудник'))
    branch = forms.CharField(label=_('Филиал'))
    
    class Meta:
        model = MoneyTransfer
        fields =('trade_partner', 'loan', 'employee', 'branch', 'transfer_amount')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Field('trade_partner', wrapper_class='form-group col-md-12 mb-0', autocomplete='off', readonly=True),
                Field('loan', wrapper_class='form-group col-md-4 mb-0', autocomplete='off', readonly=True),
                Field('employee', wrapper_class='form-group col-md-4 mb-0', autocomplete='off', readonly=True),
                Field('branch', wrapper_class='form-group col-md-4 mb-0', autocomplete='off', readonly=True),
                Field('transfer_amount', wrapper_class='form-group col-md-12 mb-0', autocomplete='off', readonly=True),
                css_class='form-row'
            ),
        )
        

class MoneyTransferUpdateForm(forms.ModelForm):
    
    class Meta:
        model = MoneyTransfer
        fields =('is_transfered',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Field('is_transfered', wrapper_class='form-group col-md-12 mb-0', autocomplete='off'),
                css_class='form-row'
            ),
        )
