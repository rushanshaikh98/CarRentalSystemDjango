from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserDetails(models.Model):
    """Class for adding the table users into the database"""
    db_table = "users"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.ForeignKey('main.City', on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    fine_pending = models.BooleanField(default=False)


class UserVerification(models.Model):
    """Class for adding the table user_verification into the database"""
    db_table = 'user_verification'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id_proof = models.ImageField(null=True)
    approval = models.CharField(max_length=60, null=False)
    date = models.DateField(default=datetime.utcnow, null=False)


class Temporary(models.Model):
    """Class for adding the table temporary into the database"""
    db_table = 'temporary'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking_time = models.DateField(default=datetime.utcnow, null=False)
    rent_from = models.DateField(null=False)
    rent_till = models.DateField(null=False)
    city = models.ForeignKey('main.City', on_delete=models.CASCADE)
