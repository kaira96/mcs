from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Field, HTML


from .models import LoanConsultation, LoanApplication


class DateInput(forms.DateInput):
    input_type = 'date'


class LoanConsultationForm(forms.ModelForm):
    class Meta:
        model = LoanConsultation
        widgets = {'start_date': DateInput()}
        fields = (
            'loan_product', 'funding_amount', 'funding_period', 
            'first_instalment', 'is_re_financing', 'is_employer',
            'is_gurantor', 'start_date'
            )
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Field('loan_product', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),
                Field('start_date', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),
            ),
            Row(
                Field('funding_amount', wrapper_class='form-group col-md-4  mb-0', autocomplete='off'),
                Field('funding_period', wrapper_class='form-group col-md-4  mb-0', autocomplete='off'),
                Field('first_instalment', wrapper_class='form-group col-md-4  mb-0', autocomplete='off'),
            ),
            Row(
                Field('is_re_financing', wrapper_class='form-group col-md-4  mb-0', autocomplete='off'),
                Field('is_employer', wrapper_class='form-group col-md-4  mb-0', autocomplete='off'),
                Field('is_gurantor', wrapper_class='form-group col-md-4  mb-0', autocomplete='off'),
            ),
        )


class LoanConsultationDetailForm(forms.ModelForm):
    class Meta:
        model = LoanConsultation
        widgets = {'start_date': DateInput()}
        fields = (
            'loan_product', 'funding_amount', 'funding_period', 
            'first_instalment', 'monthly_payment', 'bank_surcharge', 'total_cost_with_surcharge', 'is_re_financing', 'is_employer',
            'is_gurantor', 'start_date'
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Field('loan_product', wrapper_class='form-group col-md-6  mb-0', autocomplete='off', readonly=True),
                Field('start_date', wrapper_class='form-group col-md-6  mb-0', autocomplete='off', readonly=True),
            ),
            Row(
                Field('funding_amount', wrapper_class='form-group col-md-4  mb-0', autocomplete='off', readonly=True),
                Field('funding_period', wrapper_class='form-group col-md-4  mb-0', autocomplete='off', readonly=True),
                Field('first_instalment', wrapper_class='form-group col-md-4  mb-0', autocomplete='off', readonly=True),
            ),
            Row(
                Field('monthly_payment', wrapper_class='form-group col-md-4  mb-0', autocomplete='off', readonly=True),
                Field('bank_surcharge', wrapper_class='form-group col-md-4  mb-0', autocomplete='off', readonly=True),
                Field('total_cost_with_surcharge', wrapper_class='form-group col-md-4  mb-0', autocomplete='off', readonly=True),
            ),
            Row(
                Field('is_re_financing', wrapper_class='form-group col-md-4  mb-0', autocomplete='off', readonly=True),
                Field('is_employer', wrapper_class='form-group col-md-4  mb-0', autocomplete='off', readonly=True),
                Field('is_gurantor', wrapper_class='form-group col-md-4  mb-0', autocomplete='off', readonly=True),
            )
        )
        

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = ('funding_amount', 'funding_period', 'bank_surcharge', 'first_instalment',
                  'total_cost_with_surcharge', 'monthly_payment', 'loan_product')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                HTML("""
                        <div class="form-group col-md-12 mb-0">
                            <div id="div_id_loan_product" class="form-group">
                                <label for="id_loan_product" class=" requiredField">Кредитный продукт
                                    <span class="asteriskField">*</span>
                                </label>
                                <div>
                                    <select name="loan_product" class="select custom-select" id="id_loan_product">
                                        {% for loan_product in loan_products %}
                                            <option value="{{loan_product.id}}" 
                                                    data-percent="{{loan_product.percent}}">
                                                    {{loan_product.name}}
                                            </option>
                                        {% endfor %}
                                    </select>
                                </div>
                            </div>
                        </div>
                    """
                     ),
                Field('funding_amount', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('funding_period', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),

                Field('first_instalment', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('bank_surcharge', wrapper_class='form-group col-md-6 mb-0', autocomplete='off', editable=False),

                Field('total_cost_with_surcharge', wrapper_class='form-group col-md-6 mb-0', autocomplete='off', editable=False),
                Field('monthly_payment', wrapper_class='form-group col-md-6 mb-0', autocomplete='off', editable=False),
                css_class='form-row'
            ),
        )

