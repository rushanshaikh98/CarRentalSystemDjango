from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class CarModels(models.Model):
    """Class for adding the table car_models into the database"""
    db_table = 'car_models'

    model_name = models.CharField(max_length=60, null=False)


class CarCompany(models.Model):
    """Class for adding the table car_companies into the database"""
    db_table = 'car_companies'

    company_name = models.CharField(max_length=60, null=False)


class CarCategories(models.Model):
    """Class for adding the table car_categories into the database"""
    db_table = 'car_categories'

    category = models.CharField(max_length=60, null=False)


class Car(models.Model):
    """Class for adding the table cars into the database"""
    db_table = 'cars'

    number_plate = models.CharField(max_length=20, null=False)
    company = models.ForeignKey(CarCompany, on_delete=models.CASCADE)
    category = models.ForeignKey(CarCategories, on_delete=models.CASCADE)
    model = models.ForeignKey(CarModels, on_delete=models.CASCADE)
    color = models.CharField(max_length=60, null=False)
    mileage = models.IntegerField(null=False)
    ppd = models.IntegerField(null=False)
    min_rent = models.IntegerField(null=False)
    city = models.ForeignKey('main.City', on_delete=models.CASCADE)
    deposit = models.IntegerField(null=False)
    status = models.CharField(max_length=60, null=False, default=True)


class Rented(models.Model):
    """Class for adding the table rented into the database"""
    db_table = 'rented'

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_time = models.DateField(default=datetime.utcnow, null=False)
    rent_from = models.DateField(null=False)
    rent_till = models.DateField(null=False)
    car_taken = models.BooleanField(default=False)
    car_delivery = models.BooleanField(default=False)
    city_taken = models.ForeignKey('main.City', on_delete=models.CASCADE, related_name='city_taken')
    city_delivery = models.ForeignKey('main.City', on_delete=models.CASCADE, related_name='city_delivery')
    final_status = models.CharField(max_length=60, null=False, default=True)
    said_date = models.BooleanField(default=True)
    said_time = models.BooleanField(default=True)
    proper_condition = models.BooleanField(default=True)
    description = models.CharField(max_length=200)
    fine = models.IntegerField(null=False, default=0)
    fine_paid = models.BooleanField(default=False)


class Maintenance(models.Model):
    """Class for adding the table maintenance into the database"""
    db_table = 'maintenance'

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.utcnow, null=False)
    description = models.CharField(max_length=200, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
