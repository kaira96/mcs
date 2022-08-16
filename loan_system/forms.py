from django import forms
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Field, HTML, Submit


from .models import LoanConsultation, LoanApplication, SocialAnalysis, LoanApplicationConfirmHistory, Loan


class DateInput(forms.DateInput):
    input_type = 'date'


class LoanConsultationForm(forms.ModelForm):
    class Meta:
        model = LoanConsultation
        widgets = {'start_date': DateInput(format='%Y-%m-%d')}
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
        widgets = {'start_date': DateInput(format='%Y-%m-%d')}
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
                Field('funding_amount', wrapper_class='form-group col-md-6 mb-0', autocomplete='off', readonly=True),
                Field('funding_period', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),

                Field('first_instalment', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('bank_surcharge', wrapper_class='form-group col-md-6 mb-0', autocomplete='off', editable=False),

                Field('total_cost_with_surcharge', wrapper_class='form-group col-md-6 mb-0', autocomplete='off', editable=False),
                Field('monthly_payment', wrapper_class='form-group col-md-6 mb-0', autocomplete='off', editable=False),
                Submit(name='submit', value='Сохранить', css_class='su  form-group form-control btn btn-success'),
                css_class='form-row'
            ),
        )


class LoanApplicationConclusionForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = ('give_out_status',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Field('give_out_status', wrapper_class='form-group col-md-12 mb-0', autocomplete='off'),
                css_class='form-row'
            ),
        )


class LoanApplicationConclusionConfirmForm(forms.ModelForm):
    class Meta:
        model = LoanApplicationConfirmHistory
        fields = ('is_confirm',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Field('is_confirm', wrapper_class='form-group col-md-12 mb-0', autocomplete='off'),
                css_class='form-row'
            ),
        )


class SocialAnalysisReadForm(forms.ModelForm):
    full_name = forms.CharField(
        label='Фамилия, имя, отчество клиента',
        disabled=True,
        required=False   
    )
    age = forms.IntegerField(
        label='Возраст клиента (в годах)',
        disabled=True,
        required=False
    )
    is_married = forms.CharField(
        label='Семейное положение',
        disabled=True,
        required=False
    )
    education = forms.CharField(
        label='Образование',
        disabled=True,
        required=False
    )
    minor_children_amount = forms.IntegerField(
        label='количество несовершеннолетних детей',
        disabled=True,
        required=False
    )
    adult_children_amount = forms.IntegerField(
        label='количество совершеннолетних детей',
        disabled=True,
        required=False
    )
    duration_work_at_current_place = forms.IntegerField(
        label='срок работы на текущем месте (в мес.)',
        disabled=True,
        required=False
    )
    duration_work_at_previus_place = forms.IntegerField(
        label='срок работы на предыдущем месте (в мес.)',
        disabled=True,
        required=False
    )
    duration_work_at_penultimate_place = forms.IntegerField(
        label='срок работы на предпоследнем месте (в мес.)',
        disabled=True,
        required=False
    )
    is_for_hire = forms.CharField(
        label='клиент работает по найму',
        disabled=True,
        required=False
    )
    type_of_commercial_activity = forms.CharField(
        label='Вид комерческой деятельности',
        disabled=True,
        required=False
    )
    is_judged = forms.CharField(
        label='Есть ли судимость',
        disabled=True,
        required=False
    )
    
    class Meta:
        model = SocialAnalysis
        fields = ('profession_relevance', 'is_match', 'client_loans_history',
                  'own_house_address', 'has_a_car', 'сlient_behavior',
                  'is_swear', 'is_sharia_type_of_activity')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.attrs = {'novalidate': ''}

        self.helper.layout = Layout(
            Row(
                Field('full_name', wrapper_class='form-group col-md-8 mb-2', autocomplete='off', readonly=True),
                
                Field('age', wrapper_class='form-group col-md-4 mb-2', autocomplete='off', readonly=True),
            
                Field('is_married', wrapper_class='form-group col-md-6 mb-2', autocomplete='off', readonly=True),
                
                Field('education', wrapper_class='form-group col-md-6 mb-2', autocomplete='off', readonly=True),

                Field('minor_children_amount', wrapper_class='form-group col-md-6 mb-2', autocomplete='off', readonly=True),
                
                Field('adult_children_amount', wrapper_class='form-group col-md-6 mb-2', autocomplete='off', readonly=True),
                
                Field('duration_work_at_current_place', wrapper_class='form-group col-md-4  mb-2', autocomplete='off', readonly=True),
                
                Field('duration_work_at_previus_place', wrapper_class='form-group col-md-4  mb-2', autocomplete='off', readonly=True),
                
                Field('duration_work_at_penultimate_place', wrapper_class='form-group col-md-4  mb-2', autocomplete='off', readonly=True),

                Field('is_for_hire', wrapper_class='form-group col-md-4  mb-2', autocomplete='off', readonly=True),
                
                Field('type_of_commercial_activity', wrapper_class='form-group col-md-4  mb-2', autocomplete='off', readonly=True),

                Field('is_judged', wrapper_class='form-group col-md-4  mb-2', autocomplete='off', readonly=True),
                
                Field('profession_relevance', wrapper_class='form-group col-md-6  mb-4', autocomplete='off', readonly=True),
                
                Field('сlient_behavior', wrapper_class='form-group col-md-6  mb-4', autocomplete='off', readonly=True),
                
                Field('is_match', wrapper_class='form-group col-md-6  mb-2', autocomplete='off', readonly=True),
                
                Field('client_loans_history', wrapper_class='form-group col-md-6  mb-2 ', autocomplete='off', readonly=True),
                
                Field('own_house_address', wrapper_class='form-group col-md-6  mb-4', autocomplete='off', readonly=True),
                
                Field('has_a_car', wrapper_class='form-group col-md-6  mb-2', autocomplete='off', readonly=True),
                                
                Field('is_swear', wrapper_class='form-group col-md-6 mb-2', autocomplete='off', readonly=True),
                
                Field('is_sharia_type_of_activity', wrapper_class='form-group col-md-6  mb-2', autocomplete='off', readonly=True)),
        )
        
        
class SocialAnalysisForm(forms.ModelForm):
    full_name = forms.CharField(
        label='Фамилия, имя, отчество клиента',
        disabled=True,
        required=False   
    )
    age = forms.IntegerField(
        label='Возраст клиента (в годах)',
        disabled=True,
        required=False
    )
    is_married = forms.CharField(
        label='Семейное положение',
        disabled=True,
        required=False
    )
    education = forms.CharField(
        label='Образование',
        disabled=True,
        required=False
    )
    minor_children_amount = forms.IntegerField(
        label='количество несовершеннолетних детей',
        disabled=True,
        required=False
    )
    adult_children_amount = forms.IntegerField(
        label='количество совершеннолетних детей',
        disabled=True,
        required=False
    )
    duration_work_at_current_place = forms.IntegerField(
        label='срок работы на текущем месте (в мес.)',
        disabled=True,
        required=False
    )
    duration_work_at_previus_place = forms.IntegerField(
        label='срок работы на предыдущем месте (в мес.)',
        disabled=True,
        required=False
    )
    duration_work_at_penultimate_place = forms.IntegerField(
        label='срок работы на предпоследнем месте (в мес.)',
        disabled=True,
        required=False
    )
    is_for_hire = forms.CharField(
        label='клиент работает по найму',
        disabled=True,
        required=False
    )
    type_of_commercial_activity = forms.CharField(
        label='Вид комерческой деятельности',
        disabled=True,
        required=False
    )
    is_judged = forms.CharField(
        label='Есть ли судимость',
        disabled=True,
        required=False
    )
    
    class Meta:
        model = SocialAnalysis
        fields = ('profession_relevance', 'is_match', 'client_loans_history',
                  'own_house_address', 'has_a_car', 'сlient_behavior',
                  'is_swear', 'is_sharia_type_of_activity')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.attrs = {'novalidate': ''}

        self.helper.layout = Layout(
            Row(
                Field('full_name', wrapper_class='form-group col-md-8 mb-2', autocomplete='off'),
                
                Field('age', wrapper_class='form-group col-md-4 mb-2', autocomplete='off'),
            
                Field('is_married', wrapper_class='form-group col-md-6 mb-2', autocomplete='off'),
                
                Field('education', wrapper_class='form-group col-md-6 mb-2', autocomplete='off'),

                Field('minor_children_amount', wrapper_class='form-group col-md-6 mb-2', autocomplete='off'),
                
                Field('adult_children_amount', wrapper_class='form-group col-md-6 mb-2', autocomplete='off'),
                
                Field('duration_work_at_current_place', wrapper_class='form-group col-md-4  mb-2', autocomplete='off'),
                
                Field('duration_work_at_previus_place', wrapper_class='form-group col-md-4  mb-2', autocomplete='off'),
                
                Field('duration_work_at_penultimate_place', wrapper_class='form-group col-md-4  mb-2', autocomplete='off'),

                Field('is_for_hire', wrapper_class='form-group col-md-4  mb-2', autocomplete='off'),
                
                Field('type_of_commercial_activity', wrapper_class='form-group col-md-4  mb-2', autocomplete='off'),

                Field('is_judged', wrapper_class='form-group col-md-4  mb-2', autocomplete='off'),
                
                Field('profession_relevance', wrapper_class='form-group col-md-6  mb-4', autocomplete='off'),
                
                Field('сlient_behavior', wrapper_class='form-group col-md-6  mb-4', autocomplete='off'),
                
                Field('is_match', wrapper_class='form-group col-md-6  mb-2', autocomplete='off'),
                
                Field('client_loans_history', wrapper_class='form-group col-md-6  mb-2 ', autocomplete='off'),
                
                Field('own_house_address', wrapper_class='form-group col-md-6  mb-4', autocomplete='off'),
                
                Field('has_a_car', wrapper_class='form-group col-md-6  mb-2', autocomplete='off'),
                                
                Field('is_swear', wrapper_class='form-group col-md-6 mb-2', autocomplete='off'),
                
                Field('is_sharia_type_of_activity', wrapper_class='form-group col-md-6  mb-2', autocomplete='off')),
        )


class LoanForm(forms.ModelForm):

    is_overdue = forms.CharField(label=_('просрочено'),)
    
    class Meta:
        model = Loan
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        
        self.helper.layout = Layout(
            Row(
                Field('classification', wrapper_class='form-group col-md-6 mb-0', autocomplete='off', readonly=True),
                Field('classification_percent', wrapper_class='form-group col-md-6 mb-0', autocomplete='off', readonly=True),
                css_class='form-row'
            ),
            Row(
                Field('urgent_principal_debt', wrapper_class='form-group col-md-3 mb-0', autocomplete='off', readonly=True),
                Field('overdue_principal_debt', wrapper_class='form-group col-md-3 mb-0', autocomplete='off', readonly=True),
                Field('overdue_days_quantity', wrapper_class='form-group col-md-3 mb-0', autocomplete='off', readonly=True),
                Field('total_overdue_days_quantity', wrapper_class='form-group col-md-3 mb-0', autocomplete='off', readonly=True),
                css_class='form-row'
            ),
            Row(
                Field('is_overdue', wrapper_class='form-group col-md-6 mb-0', autocomplete='off', readonly=True),
                Field('accrual_status_date', wrapper_class='form-group col-md-6 mb-0', autocomplete='off', readonly=True),
                css_class='form-row'
            ),
        )
        