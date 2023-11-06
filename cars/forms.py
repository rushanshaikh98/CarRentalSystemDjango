from django import forms
from django.apps import apps
from django.core.exceptions import ValidationError

City = apps.get_model('main', 'City')
CarCompany = apps.get_model('cars', 'CarCompany')
CarCategories = apps.get_model('cars', 'CarCategories')
CarModels = apps.get_model('cars', 'CarModels')
Car = apps.get_model('cars', 'Car')


def get_city_choices():
    return [(valve.id, valve.city) for valve in City.objects.all()]


def get_company_choices():
    return [(valve.id, valve.company_name) for valve in CarCompany.objects.all()]


def get_category_choices():
    return [(valve.id, valve.category) for valve in CarCategories.objects.all()]


def get_model_choices():
    return [(valve.id, valve.model_name) for valve in CarModels.objects.all()]


class CreateCars(forms.Form):
    """Form for taking the details of a car from the admin to add a car in the Car model"""
    number_plate = forms.CharField(label='Number Plate', required=True, max_length=20)
    company = forms.ChoiceField(required=True, widget=forms.Select, choices=get_company_choices)
    category = forms.ChoiceField(required=True, widget=forms.Select, choices=get_category_choices)
    model = forms.ChoiceField(required=True, widget=forms.Select, choices=get_model_choices)
    city = forms.ChoiceField(required=True, widget=forms.Select, choices=get_city_choices)
    color = forms.CharField(label='Color', required=True)
    mileage = forms.IntegerField(label='Mileage', required=True)
    ppd = forms.IntegerField(label='Price Per Day', required=True)
    min_rent = forms.IntegerField(label='Minimum Rent', required=True)
    deposit = forms.IntegerField(label='Deposit Amount', required=True)

    def clean(self):
        cleaned_data = super().clean()
        car = Car.objects.filter(number_plate=cleaned_data['number_plate'])
        if car:
            raise ValidationError('Car with this number plate already exists!')


class GetCar(forms.Form):
    """Form for taking the car id from the admin to get a car for different purposes"""
    number_plate = forms.CharField(label='Number Plate', required=True, max_length=20)


class UpdateCar(forms.Form):
    """Form for taking the details of a car from the admin to update it in the Car model"""
    color = forms.CharField(label='Color', required=True)
    mileage = forms.IntegerField(label='Mileage', required=True)
    ppd = forms.IntegerField(label='Price Per Day', required=True)
    min_rent = forms.IntegerField(label='Minimum Rent', required=True)
    deposit = forms.IntegerField(label='Deposit Amount', required=True)
    city = forms.ChoiceField(required=True, widget=forms.Select, choices=get_city_choices)
    status = forms.CharField(label='Final Status', required=True)


class ReturnCar(forms.Form):
    """Form for entering the details of the car after it is reviewed by the admin"""
    TRUE_FALSE_CHOICES = ((True, 'Yes'), (False, 'No'))
    said_date = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, label="Said Date", initial='', widget=forms.Select(),
                                  required=True)
    said_time = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, label="Said Time", initial='', widget=forms.Select(),
                                  required=True)
    proper_condition = forms.ChoiceField(choices=TRUE_FALSE_CHOICES, label="Proper Condition", initial='',
                                         widget=forms.Select(), required=True)
    description = forms.CharField(label='Description', required=False)
    fine = forms.IntegerField(label='Fine Amount', initial=0, required=True)


class CarMaintenance(forms.Form):
    """Form for accepting the description of the car from admin for maintaining it"""
    description = forms.CharField(label='Description', required=True)
