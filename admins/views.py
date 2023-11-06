from django.apps import apps
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import (CreateAdmins, AddCity, UpdateCity, DeleteCity, AddCompany, UpdateCompany, DeleteCompany,
                    AddCategory, UpdateCategory, DeleteCategory, AddModel, UpdateModel, DeleteModel)

City = apps.get_model('main', 'City')
UserDetails = apps.get_model('users', 'UserDetails')
CarCompany = apps.get_model('cars', 'CarCompany')
Car = apps.get_model('cars', 'Car')
CarCategories = apps.get_model('cars', 'CarCategories')
CarModels = apps.get_model('cars', 'CarModels')
UserVerification = apps.get_model('users', 'UserVerification')


# Create your views here.

@user_passes_test(lambda u: u.is_superuser)
def create_admins(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    if request.method == "POST":
        form = CreateAdmins(request.POST)
        if form.is_valid():
            user = form.save()
            user_details = UserDetails(user_id=user.id, city_id=form.cleaned_data.get('city'))
            user_details.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('main-home')
    else:
        form = CreateAdmins()
    return render(request, 'register.html', {'form': form})


def admin_list(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    admins_list = User.objects.filter(is_staff=True).filter(is_superuser=False).all()
    if admins_list:
        return render(request, 'admin_list.html', {'admins_list': admins_list})
    else:
        messages.info(request, "There are no admins!")
        return redirect('main-home')


@user_passes_test(lambda u: u.is_superuser)
def delete_admin(request, user_id):
    User.objects.filter(id=user_id).delete()
    messages.success(request, 'Admin has been deleted successfully!')
    return redirect('main-home')


@user_passes_test(lambda u: u.is_superuser)
def add_city(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    if request.method == 'POST':
        form = AddCity(request.POST)
        if form.is_valid():
            cities = City.objects.filter(city=form.cleaned_data.get('city').replace(" ", "").upper())
            if cities:
                messages.error(request, 'City with this name already exists!')
            else:
                city = City(city=form.cleaned_data.get('city').replace(" ", "").upper())
                city.save()
                messages.success(request, 'City has been added successfully!')
            return redirect('add_city')
    else:
        form = AddCity()
    return render(request, 'form.html', {'form': form, 'title': 'Add City', 'button': 'Add!'})


@user_passes_test(lambda u: u.is_superuser)
def update_city(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""
    cities = City.objects.all()
    if cities:
        if request.method == 'POST':
            form = UpdateCity(request.POST)
            if form.is_valid():
                cities = City.objects.filter(city=form.cleaned_data.get('city').replace(" ", "").upper())
                if cities:
                    messages.error(request, 'City with this name already exists!')
                else:
                    city = City.objects.filter(id=form.cleaned_data.get('city_id')).first()
                    city.city = form.cleaned_data.get('city').replace(" ", "").upper()
                    city.save()
                    messages.success(request, 'City has been updated successfully!')
                return redirect('main-home')
        else:
            form = UpdateCity()
        return render(request, 'form.html', {'form': form, 'title': 'Update City', 'button': 'Update!'})
    else:
        messages.error(request, 'There are no cities!')
        return redirect('main-home')


@user_passes_test(lambda u: u.is_superuser)
def delete_city(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    cities = City.objects.all()
    if cities:
        if request.method == "POST":
            form = DeleteCity(request.POST)
            if form.is_valid():
                users = UserDetails.objects.filter(city_id=form.cleaned_data.get('city_id')).first()
                if users:
                    messages.error(request, "City cannot be deleted as it has users!")
                else:
                    City.objects.filter(id=form.cleaned_data.get('city_id')).delete()
                    messages.success(request, 'City has been deleted successfully!')
                return redirect('main-home')
        else:
            form = DeleteCity()
        return render(request, 'form.html', {'form': form, 'title': 'Delete City', 'button': 'Delete!'})
    else:
        messages.error(request, 'There are no cities!')
        return redirect('main-home')


@user_passes_test(lambda u: u.is_superuser)
def add_company(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    if request.method == 'POST':
        form = AddCompany(request.POST)
        if form.is_valid():
            companies = CarCompany.objects.filter(
                company_name=form.cleaned_data.get('company').replace(" ", "").upper())
            if companies:
                messages.error(request, 'Company with this name already exists!')
            else:
                company = CarCompany(company_name=form.cleaned_data.get('company').replace(" ", "").upper())
                company.save()
                messages.success(request, 'Company has been added successfully!')
            return redirect('add_company')
    else:
        form = AddCompany()
    return render(request, 'form.html', {'form': form, 'title': 'Add Company', 'button': 'Add!'})


@user_passes_test(lambda u: u.is_superuser)
def update_company(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    companies = CarCompany.objects.all()
    if companies:
        if request.method == 'POST':
            form = UpdateCompany(request.POST)
            if form.is_valid():
                companies = CarCompany.objects.filter(
                    company_name=form.cleaned_data.get('company').replace(" ", "").upper())
                if companies:
                    messages.error(request, 'Company with this name already exists!')
                else:
                    company = CarCompany.objects.filter(id=form.cleaned_data.get('company_id')).first()
                    company.company_name = form.cleaned_data.get('company').replace(" ", "").upper()
                    company.save()
                    messages.success(request, 'Company has been updated successfully!')
                return redirect('main-home')
        else:
            form = UpdateCompany()
        return render(request, 'form.html', {'form': form, 'title': 'Update Company', 'button': 'Update!'})
    else:
        messages.error(request, 'There are no companies!')
        return redirect('main-home')


@user_passes_test(lambda u: u.is_superuser)
def delete_company(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    companies = CarCompany.objects.all()
    if companies:
        if request.method == "POST":
            form = DeleteCompany(request.POST)
            if form.is_valid():
                cars = Car.objects.filter(company_id=form.cleaned_data.get('company_id')).first()
                if cars:
                    messages.error(request, "Company cannot be deleted as our company owns some cars of this company!")
                else:
                    CarCompany.objects.filter(id=form.cleaned_data.get('company_id')).delete()
                    messages.success(request, 'Company has been deleted successfully!')
                return redirect('main-home')
        else:
            form = DeleteCompany()
        return render(request, 'form.html', {'form': form, 'title': 'Delete Company', 'button': 'Delete!'})
    else:
        messages.error(request, 'There are no companies!')
        return redirect('main-home')


@user_passes_test(lambda u: u.is_superuser)
def add_category(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    if request.method == 'POST':
        form = AddCategory(request.POST)
        if form.is_valid():
            categories = CarCategories.objects.filter(
                category=form.cleaned_data.get('category').replace(" ", "").upper())
            if categories:
                messages.error(request, 'Category with this name already exists!')
            else:
                category = CarCategories(category=form.cleaned_data.get('category').replace(" ", "").upper())
                category.save()
                messages.success(request, 'Category has been added successfully!')
            return redirect('add_category')
    else:
        form = AddCategory()
    return render(request, 'form.html', {'form': form, 'title': 'Add Category', 'button': 'Add!'})


@user_passes_test(lambda u: u.is_superuser)
def update_category(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    categories = CarCategories.objects.all()
    if categories:
        if request.method == 'POST':
            form = UpdateCategory(request.POST)
            if form.is_valid():
                categories = CarCategories.objects.filter(
                    category=form.cleaned_data.get('category').replace(" ", "").upper())
                if categories:
                    messages.error(request, 'Category with this name already exists!')
                else:
                    category = CarCategories.objects.filter(id=form.cleaned_data.get('category_id')).first()
                    category.category = form.cleaned_data.get('category').replace(" ", "").upper()
                    category.save()
                    messages.success(request, 'Category has been updated successfully!')
                return redirect('main-home')
        else:
            form = UpdateCategory()
        return render(request, 'form.html', {'form': form, 'title': 'Update Category', 'button': 'Update!'})
    else:
        messages.error(request, 'There are no categories!')
        return redirect('main-home')


@user_passes_test(lambda u: u.is_superuser)
def delete_category(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    categories = CarCompany.objects.all()
    if categories:
        if request.method == "POST":
            form = DeleteCategory(request.POST)
            if form.is_valid():
                cars = Car.objects.filter(category_id=form.cleaned_data.get('category_id')).first()
                if cars:
                    messages.error(request,
                                   "Category cannot be deleted as our company owns some cars of this category!")
                else:
                    CarCategories.objects.filter(id=form.cleaned_data.get('category_id')).delete()
                    messages.success(request, 'Category has been deleted successfully!')
                return redirect('main-home')
        else:
            form = DeleteCategory()
        return render(request, 'form.html', {'form': form, 'title': 'Delete Category', 'button': 'Delete!'})
    else:
        messages.error(request, 'There are no categories!')
        return redirect('main-home')


@user_passes_test(lambda u: u.is_superuser)
def add_model(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    if request.method == 'POST':
        form = AddModel(request.POST)
        if form.is_valid():
            models = CarModels.objects.filter(model_name=form.cleaned_data.get('model').replace(" ", "").upper())
            if models:
                messages.error(request, 'Model with this name already exists!')
            else:
                model = CarModels(model_name=form.cleaned_data.get('model').replace(" ", "").upper())
                model.save()
                messages.success(request, 'Model has been added successfully!')
            return redirect('add_model')
    else:
        form = AddModel()
    return render(request, 'form.html', {'form': form, 'title': 'Add Model', 'button': 'Add!'})


@user_passes_test(lambda u: u.is_superuser)
def update_model(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    models = CarModels.objects.all()
    if models:
        if request.method == 'POST':
            form = UpdateModel(request.POST)
            if form.is_valid():
                models = CarModels.objects.filter(model_name=form.cleaned_data.get('model').replace(" ", "").upper())
                if models:
                    messages.error(request, 'Model with this name already exists!')
                else:
                    model = CarModels.objects.filter(id=form.cleaned_data.get('model_id')).first()
                    model.model_name = form.cleaned_data.get('model').replace(" ", "").upper()
                    model.save()
                    messages.success(request, 'Model has been updated successfully!')
                return redirect('main-home')
        else:
            form = UpdateModel()
        return render(request, 'form.html', {'form': form, 'title': 'Update Model', 'button': 'Update!'})
    else:
        messages.error(request, 'There are no models!')
        return redirect('main-home')


@user_passes_test(lambda u: u.is_superuser)
def delete_model(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    models = CarModels.objects.all()
    if models:
        if request.method == "POST":
            form = DeleteModel(request.POST)
            if form.is_valid():
                cars = Car.objects.filter(model_id=form.cleaned_data.get('model_id')).first()
                if cars:
                    messages.error(request, "Model cannot be deleted as our company owns some cars of this model!")
                else:
                    CarModels.objects.filter(id=form.cleaned_data.get('model_id')).delete()
                    messages.success(request, 'Model has been deleted successfully!')
                return redirect('main-home')
        else:
            form = DeleteModel()
        return render(request, 'form.html', {'form': form, 'title': 'Delete Model', 'button': 'Delete!'})
    else:
        messages.error(request, 'There are no models!')
        return redirect('main-home')


@user_passes_test(lambda u: u.is_staff)
def view_image(request, img):
    """Method to display the details and image uploaded by a user for the verification by selecting a specific users
    from many users which can only be accessed by the admin.
    -----------------------------
    Returns: Details of the user and the id proof image he has submitted with buttons to review the request"""

    image_path = settings.MEDIA_ROOT + '/' + img
    with open(image_path, 'rb') as image_file:
        return HttpResponse(request, image_file, content_type='image/jpeg')


@user_passes_test(lambda u: u.is_staff)
def accept_user(request, user_id):
    """Method to approve the verification request by the user which can only be accessed by the admin. It is called
    when the accept button in verify user method is clicked. It also enters the user as verified in the database.
    -----------------------------
    Returns: The success flash message and redirects again to requests list"""

    user_ver = UserVerification.objects.filter(user_id=user_id).filter(approval="").first()
    user = UserDetails.objects.filter(user_id=user_id).first()
    user.is_verified = True
    user_ver.approval = "true"
    user.save()
    user_ver.save()
    messages.success(request, 'User successfully verified!')
    return redirect('display_users_list')


@user_passes_test(lambda u: u.is_staff)
def reject_user(request, user_id):
    """Method to reject the verification request by the user which can only be accessed by the admin. It is called
    when the reject button in verify user method is clicked. It also enters the user as rejected in the database.
    -----------------------------
    Returns: The danger flash message and redirects again to requests list"""

    user_ver = UserVerification.objects.filter(user_id=user_id).filter(approval="").first()
    user_ver.approval = "false"
    user_ver.save()
    messages.warning(request, 'User successfully rejected!')
    return redirect('display_users_list')
