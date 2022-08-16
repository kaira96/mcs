from django import forms
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Field

from .models import Deposit


class DepositForm(forms.ModelForm):
    
    class Meta:
        model = Deposit
        fields = ('current_balance', 'date_of_last_deposit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        
        self.helper.layout = Layout(
            Row(
                Field('current_balance', wrapper_class='form-group col-md-6 mb-0', autocomplete='off', readonly=True),
                Field('date_of_last_deposit', wrapper_class='form-group col-md-6 mb-0', autocomplete='off', readonly=True),
                css_class='form-row'
            ),
        )


class DepositPayForm(forms.Form):
    number = forms.IntegerField(
        label=_('Номер счёта'),
        disabled=True,
        required=False  
    )
    top_up_amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=10,
        label=_('Сумма пополнения')
    )


class DepositDetailForm(forms.ModelForm):
    account_number = forms.CharField(
        required=False
    )
    balance_account = forms.CharField(
        required=False
    )
    branch = forms.CharField(
        required=False
    )
    employee = forms.CharField(
        required=False
    )
    is_active = forms.CharField(
        required=False
    )
    is_blocked = forms.CharField(
        required=False
    )
    client = forms.CharField(
        label=_('Клиент'),
        required=False
    )
    current_balance = forms.DecimalField(
        required=False
    )
    
    class Meta:
        model = Deposit
        fields = ('client', 'current_balance', 'date_of_last_deposit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        
        self.helper.layout = Layout(
            Row(
                Field('client', wrapper_class='form-group col-md-12 mb-0', autocomplete='off', readonly=True),
                Field('current_balance', wrapper_class='form-group col-md-6 mb-0', autocomplete='off', readonly=True),
                Field('date_of_last_deposit', wrapper_class='form-group col-md-6 mb-0', autocomplete='off', readonly=True),
                css_class='form-row'
            ),
        )


class DepositAccountSearchForm(forms.Form):
    
    deposit_account_number = forms.IntegerField(
        min_value=0,
        label=_('Введите № депозитного счёта')
    )
        