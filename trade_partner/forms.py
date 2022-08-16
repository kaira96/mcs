from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Field

from dal import autocomplete

from .models import ProductDetail


class ProductDetailForm(forms.ModelForm):
    class Meta:
        model = ProductDetail

        widgets = {
            'trade_partner': autocomplete.ModelSelect2(
                url='trade-partner-autocomplete',
                attrs={'data-minimum-input-length': 3}
            ),
            'category': autocomplete.ModelSelect2(
                url='category-autocomplete'
            )
        }
        
        fields = ('trade_partner', 'description', 'price', 'category', 'seller_full_name', 'seller_phone_number',
                  'first_installment_is_paid_to_TO', 'filial_point')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.attrs = {'novalidate': ''}

        self.helper.layout = Layout(
            Row(
                Field('trade_partner', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('category', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('seller_full_name', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('seller_phone_number', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('description', wrapper_class='form-group col-md-9 mb-0', autocomplete='off'),
                Field('price', wrapper_class='form-group col-md-3 mb-0', autocomplete='off'),
                Field('first_installment_is_paid_to_TO', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('filial_point', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
            )
        )


class BaseProductDetailFormSet(forms.BaseFormSet):

    def clean(self):
        return True
