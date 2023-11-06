import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def username_validation(value):
    if " " not in value:
        user = User.objects.filter(username=value).values()
        if user:
            raise ValidationError('Username is already taken!')
    else:
        raise ValidationError('Username cannot have spaces!')


def email_validation(value):
    user = User.objects.filter(email=value).values()
    if user:
        raise ValidationError('Email is already taken!')


def password_validation(passwd):
    special_chars = ['$', '@', '#', '%']
    error = ""
    if len(passwd) < 6:
        error += 'Length should be at least 6!\n'

    if len(passwd) > 20:
        error += 'Length should be not be greater than 20!\n'

    if not any(char.isdigit() for char in passwd):
        error += 'Password should have at least one numeral!\n'

    if not any(char.isupper() for char in passwd):
        error += 'Password should have at least one uppercase letter!\n'

    if not any(char.islower() for char in passwd):
        error += 'Password should have at least one lowercase letter!\n'

    if not any(char in special_chars for char in passwd):
        error += 'Password should have at least one of the symbols $@#%!\n'

    if len(error) > 0:
        raise ValidationError(f'{error}')


def validate_rent_from(value):
    """Method for validating the entered dates

    Args
    ------------------
    self: is used as the function is defined in the class
    field: It is the rent from date entered by the user which needs to validated

    Returns
    ------------------
    True if the field is validated or raises a Validation error"""

    if value < datetime.date.today():
        raise ValidationError("The date cannot be in the past!")
