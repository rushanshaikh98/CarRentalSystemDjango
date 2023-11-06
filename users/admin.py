from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .forms import RegistrationForm
from .models import UserDetails, UserVerification, Temporary


# Register your models here.
# class CustomUserAdmin(UserAdmin):
#     add_form = RegistrationForm


admin.site.register(UserDetails)
admin.site.register(UserVerification)
admin.site.register(Temporary)
# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
