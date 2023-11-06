import datetime

from django import forms
from django.apps import apps
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .validators import email_validation, validate_file_extension

City = apps.get_model('main', 'City')


def get_valve_choices():
    return [(valve.id, valve.city) for valve in City.objects.all()]


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(validators=[email_validation])

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "first_name", "last_name"]

    city = forms.ChoiceField(required=True, widget=forms.Select, choices=get_valve_choices)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class TakingDates(forms.Form):
    """Form for taking the dates from the user to book the cars"""
    rent_from = forms.DateField(widget=forms.SelectDateWidget())
    rent_till = forms.DateField(widget=forms.SelectDateWidget())
    city = forms.ChoiceField(required=True, widget=forms.Select, choices=get_valve_choices)

    def clean(self):
        cleaned_data = super().clean()
        rent_from = cleaned_data.get('rent_from')
        rent_till = cleaned_data.get('rent_till')
        if rent_from < datetime.date.today():
            raise ValidationError("The date cannot be in the past!")
        if rent_till <= rent_from:
            raise ValidationError('Rent till should be greater!')


class ApprovalForm(forms.Form):
    """Form to taking the id proof from a user to verify that user"""
    id_proof = forms.ImageField(widget=forms.ClearableFileInput(), required=True, validators=[validate_file_extension])
