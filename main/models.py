from django.db import models


# Create your models here.

class City(models.Model):
    """Class for adding the table cities into the database"""
    db_table = "cities"

    city = models.CharField(max_length=60, null=False, unique=True)
