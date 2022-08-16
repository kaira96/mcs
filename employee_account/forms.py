from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Submit
from django import forms
from django.contrib.auth.forms import AuthenticationForm, ReadOnlyPasswordHashField

from django.utils.translation import gettext_lazy as _

from .models import Employee


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_('Логин'),
    )
    password = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Column('username', css_class='form-group'),
            Column('password', css_class='form-group'),
            Submit(name='submit', value='Войти', css_class='su  form-group form-control btn btn-success')
        )


class UserCreationForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput, required=False)

    class Meta:
        model = Employee
        fields = ('password', 'login')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2
