from django.contrib import admin
from django.contrib.auth.models import User

from .models import Car, CarModels, CarCompany, CarCategories, Rented, Maintenance
# Register your models here.
admin.site.register(Car)
admin.site.register(CarModels)
admin.site.register(CarCompany)
admin.site.register(CarCategories)
admin.site.register(Maintenance)
admin.site.register(Rented)
