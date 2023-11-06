from django import forms
from django.apps import apps
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .validators import email_validation

City = apps.get_model('main', 'City')
CarCompany = apps.get_model('cars', 'CarCompany')
CarCategories = apps.get_model('cars', 'CarCategories')
CarModels = apps.get_model('cars', 'CarModels')


def get_city_choices():
    return [(valve.id, valve.city) for valve in City.objects.all()]


def get_company_choices():
    return [(valve.id, valve.company_name) for valve in CarCompany.objects.all()]


def get_category_choices():
    return [(valve.id, valve.category) for valve in CarCategories.objects.all()]


def get_model_choices():
    return [(valve.id, valve.model_name) for valve in CarModels.objects.all()]


class CreateAdmins(UserCreationForm):
    """Form to take input from the super admin to create a new admin and validating the inputs provided
    if required when clicking on the submit button else submitting the data to method/class where the is called"""

    email = forms.EmailField(validators=[email_validation])

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "first_name", "last_name"]

    city = forms.ChoiceField(required=True, widget=forms.Select, choices=get_city_choices)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff = True
        if commit:
            user.save()
        return user


class AddCity(forms.Form):
    """Form to take input of the city name from the super admin to add a new city into the City model and validating it if
    required"""
    city = forms.CharField(label='City Name', required=True)


class UpdateCity(forms.Form):
    """Form for selecting the current city and entering the new city name in order to update name of the city"""

    city_id = forms.ChoiceField(required=True, widget=forms.Select, choices=get_city_choices)
    city = forms.CharField(label=' New City Name', required=True)


class DeleteCity(forms.Form):
    """Form to take input of the city name from super admin to delete the city"""
    city_id = forms.ChoiceField(required=True, widget=forms.Select, choices=get_city_choices)


class AddCompany(forms.Form):
    """Form to take input of the company name from the super admin to add a new company into the CarCompany model and
    validating it if required"""
    company = forms.CharField(label='Company Name', required=True)


class UpdateCompany(forms.Form):
    """Form for selecting the current company and entering the new company name in order to update name of
    the company"""
    company_id = forms.ChoiceField(required=True, widget=forms.Select, choices=get_company_choices)
    company = forms.CharField(label='Company Name', required=True)


class DeleteCompany(forms.Form):
    """Form to take input of the company name from super admin to delete the company"""
    company_id = forms.ChoiceField(required=True, widget=forms.Select, choices=get_company_choices)


class AddCategory(forms.Form):
    """Form to take input of the category name from the super admin to add a new category into the
    CarCategories model and
    validating it if required"""
    category = forms.CharField(label='Category', required=True)


class UpdateCategory(forms.Form):
    """Form for selecting the current category and entering the new category name in order to update
    name of the category"""
    category_id = forms.ChoiceField(required=True, widget=forms.Select, choices=get_category_choices)
    category = forms.CharField(label='Category', required=True)


class DeleteCategory(forms.Form):
    """Form to take input of the category name from super admin to delete the category"""
    category_id = forms.ChoiceField(required=True, widget=forms.Select, choices=get_category_choices)


class AddModel(forms.Form):
    """Form to take input of the model name from the super admin to add a new model into the CarModels model and
    validating it if required"""
    model = forms.CharField(label='Model Name', required=True)


class UpdateModel(forms.Form):
    """Form for selecting the current model and entering the new model name in order to update name of the model"""
    model_id = forms.ChoiceField(required=True, widget=forms.Select, choices=get_model_choices)
    model = forms.CharField(label='Model Name', required=True)


class DeleteModel(forms.Form):
    """Form to take input of the model name from super admin to delete the model"""
    model_id = forms.ChoiceField(required=True, widget=forms.Select, choices=get_model_choices)
