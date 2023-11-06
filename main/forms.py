from django import forms
from django.apps import apps
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .validators import email_validation, password_validation

City = apps.get_model('main', 'City')


def get_valve_choices():
    return [(valve.id, valve.city) for valve in City.objects.all()]


class UpdateAccountForm(forms.ModelForm):
    """Form for taking the details of the user to update the account of the user"""
    email = forms.EmailField(label='Email')
    city = forms.ChoiceField(required=True, widget=forms.Select, choices=get_valve_choices)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if email != self.instance.email:
            email_validation(email)


class ChangePassword(forms.Form):
    """Form for taking the current and new password of the user to change the password of the user"""
    current_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput, validators=[password_validation])
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise ValidationError("Confirm password should be equal to password!")


class SearchForm(forms.Form):
    """Form for entering the search word so that the cars can be searched according to that word"""
    searched = forms.CharField(label='searched', required=True)
