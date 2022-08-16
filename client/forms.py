from crispy_forms.bootstrap import Modal
from dal import autocomplete
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Field, HTML, Div

from .models import Client, Job, ClientSalary, Spouse, Guarantor, Passport, Dependent, ClientCommercial


class DateInput(forms.DateInput):
    input_type = 'date'
    

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client

        widgets = {'date_of_birth': DateInput(format='%Y-%m-%d')}

        fields = ('first_name', 'last_name', 'middle_name',
                  'date_of_birth', 'gender', 'is_married', 'is_criminal_record',
                  'education_status', 'phone_number', 'contact_person_phone_numbers',
                  'residence_address', 'registration_address', 'is_beneficiary', 'is_political_man')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_tag = False
        self.helper.attrs = {'novalidate': ''}

        self.helper.layout = Layout(
            Row(
                Field('first_name', wrapper_class='form-group col-md-4 mb-0', autocomplete='off'),
                Field('last_name', wrapper_class='form-group col-md-4 mb-0', autocomplete='off'),
                Field('middle_name', wrapper_class='form-group col-md-4 mb-0', autocomplete='off'),

                Field('date_of_birth', wrapper_class='form-group col-md-4 mb-0', autocomplete='off'),
                Field('gender', wrapper_class='form-group col-md-4 mb-0', autocomplete='off'),
                Field('education_status', wrapper_class='form-group col-md-4 mb-0', autocomplete='off'),

                Field('phone_number', wrapper_class='form-group col-md-4 mb-0', autocomplete='off'),
                Field('residence_address', wrapper_class='form-group col-md-4 mb-0', autocomplete='off'),
                Field('registration_address', wrapper_class='form-group col-md-4 mb-0', autocomplete='off'),

                Field('contact_person_phone_numbers', wrapper_class='form-group col-md-12 mb-0', autocomplete='off'),
                css_class='form-row'
            ),
            Row(
                Field('is_married', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('is_criminal_record', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('is_beneficiary', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('is_political_man', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                css_class='form-row'
            ),
        )


class JobForm(forms.ModelForm):
    class Meta:
        model = Job

        widgets = {'date_of_employment': DateInput(format='%Y-%m-%d')}

        fields = '__all__'
        exclude = ('client',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Field('name', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('address', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('position', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),

                Field('company_definition', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('date_of_employment', wrapper_class='form-group col-md-12 mb-0', autocomplete='off'),

                Field('previous_job', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('working_period_previous_job', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('penultimate_job', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('working_period_penultimate_job', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),

                css_class='form-row'
            )
        )


class SalaryForm(forms.ModelForm):
    class Meta:
        model = ClientSalary
        fields = ('salary',)
        exclude = ('client',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Field('salary', wrapper_class='form-group col-md-12  mb-0', autocomplete='off'),
            ),
        )


class SpouseForm(forms.ModelForm):
    class Meta:
        model = Spouse
        widgets = {'date_of_birth': DateInput(format='%Y-%m-%d')}
        fields = ('first_name', 'last_name', 'middle_name', 'phone_number',
                  'job_name', 'job_position', 'education_status', 'salary',
                  'gender', 'is_guarantor', 'date_of_birth')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.attrs = {'novalidate': ''}

        self.helper.layout = Layout(
            Row(
                Field('first_name', wrapper_class='form-group col-md-4 mb-0', autocomplete='off'),
                Field('last_name', wrapper_class='form-group col-md-4 mb-0', autocomplete='off'),
                Field('middle_name', wrapper_class='form-group col-md-4 mb-0', autocomplete='off'),

                Field('phone_number', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),
                Field('date_of_birth', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('job_name', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),
                Field('job_position', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),
                Field('education_status', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),
                Field('salary', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),

                Field('gender', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),
                Field('is_guarantor', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),
            ),
        )

    def save(self, commit=True):
        super().save(commit=commit)
        if commit:
            data = self.cleaned_data
            is_guarantor = data.pop('is_guarantor')
            if is_guarantor:
                Guarantor(**data, client=self.instance.client, passport=self.instance.passport).save()

        return self.instance


class GuarantorForm(forms.ModelForm):
    class Meta:
        model = Guarantor
        widgets = {'date_of_birth': DateInput(format='%Y-%m-%d')}
        fields = ('first_name', 'last_name', 'middle_name', 'phone_number',
                  'job_name', 'job_position', 'salary', 'education_status',
                  'gender', 'residence_address', 'date_of_birth')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.attrs = {'novalidate': ''}

        self.helper.layout = Layout(
            Row(
                Field('first_name', wrapper_class='form-group col-md-4 mb-0', autocomplete='off'),
                Field('last_name', wrapper_class='form-group col-md-4 mb-0', autocomplete='off'),
                Field('middle_name', wrapper_class='form-group col-md-4 mb-0', autocomplete='off'),

                Field('residence_address', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('date_of_birth', wrapper_class='form-group col-md-6 mb-0', autocomplete='off'),
                Field('phone_number', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),
                Field('job_name', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),

                Field('job_position', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),
                Field('education_status', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),

                Field('salary', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),
                Field('gender', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),
            ),
        )


class PassportForm(forms.ModelForm):
    class Meta:
        model = Passport

        widgets = {'date_of_issue': DateInput(format='%Y-%m-%d')}

        fields = ('series', 'date_of_issue', 'pin', 'issued_it', 'series_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                HTML("""
                    <div class="form-group col-md-2 mb-0" blank="">
                        <div id="div_id_client-issued_it_mkk" class="form-group">
                          <label for="id_client-issued_it_mkk" class="">Кем выдан</label> 
                            <div> <select name="client-issued_it_mkk" class="select custom-select" id="id_client-issued_it_mkk">
                              <option value="МКК" selected="">МКК</option>
                              </select> 
                            </div> 
                        </div>
                    </div>
                """),
                Field('issued_it', wrapper_class='form-group col-md-3 mb-0', blank=True, autocomplete='off'),
                Field('series_type', wrapper_class='form-group col-md-2 mb-0', blank=True, autocomplete='off'),
                Field('series', wrapper_class='form-group col-md-5 mb-0', blank=True, autocomplete='off'),
                Field('date_of_issue', wrapper_class='form-group col-md-6 mb-0', blank=True, autocomplete='off'),
                Field('pin', wrapper_class='form-group col-md-6 mb-0', blank=True, autocomplete='off'),
                css_class='form-row'
            ),
        )


class DependentForm(forms.ModelForm):
    class Meta:
        model = Dependent
        fields = '__all__'
        exclude = ('client',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Field('children_under_18', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),
                Field('children_over_18', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),
                Field('ages', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),
                Field('another_dependents', wrapper_class='form-group col-md-6  mb-0', autocomplete='off'),
            ),
        )


class ClientCommercialForm(forms.ModelForm):
    class Meta:
        model = ClientCommercial
        fields = '__all__'
        widgets = {'start_date': DateInput(format='%Y-%m-%d')}
        exclude = ('client', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Field('salary', wrapper_class='form-group col-md-6  mb-0',
                      autocomplete='off'),
                Field('company_name', wrapper_class='form-group col-md-6  mb-0',
                      autocomplete='off'),
                Field('organization_information',
                      wrapper_class='form-group col-md-6  mb-0',
                      autocomplete='off'),
                Field('address',
                      wrapper_class='form-group col-md-6  mb-0',
                      autocomplete='off'),
                Field('license_number',
                      wrapper_class='form-group col-md-6  mb-0',
                      autocomplete='off'),
                Field('position',
                      wrapper_class='form-group col-md-6  mb-0',
                      autocomplete='off'),
                Field('start_date',
                      wrapper_class='form-group col-md-6  mb-0',
                      autocomplete='off'),
            ),
        )


class SearchClientForm(forms.ModelForm):

    class Meta:
        model = Passport
        fields = ('pin', )

        widgets = {
            'pin': autocomplete.Select2(
                url='client-autocomplete',
                attrs={'data-minimum-input-length': 5, 'data-html': False}
            ),
        }
