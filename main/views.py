import datetime

from django.apps import apps
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from .forms import ChangePassword, UpdateAccountForm, SearchForm

Temporary = apps.get_model('users', 'Temporary')
Rented = apps.get_model('cars', 'Rented')
CarCompany = apps.get_model('cars', 'CarCompany')
Car = apps.get_model('cars', 'Car')
City = apps.get_model('main', 'City')
CarCategories = apps.get_model('cars', 'CarCategories')
CarModels = apps.get_model('cars', 'CarModels')
UserDetails = apps.get_model('users', 'UserDetails')


# Create your views here.

def home(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    if request.user.is_authenticated:
        if request.user.is_staff:
            return render(request=request, template_name='home.html')

        dates = Temporary.objects.filter(user_id=request.user.id).first()
        if dates:
            if dates.rent_from < datetime.date.today():
                messages.info(request, f"Please Enter the dates again!")
                return redirect('taking_dates')
        else:
            return redirect('taking_dates')

        rented_cars = Rented.objects.filter(rent_till__gte=dates.rent_from).filter(
            rent_from__lte=dates.rent_till).filter(final_status="True").all()

        current_user = UserDetails.objects.filter(user_id=request.user.id).first()
        cars = Car.objects.filter(city_id=current_user.city_id).exclude(pk__in=rented_cars).all()
        if cars:
            paginator = Paginator(cars, 2)  # Show 25 contacts per page.

            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(request=request, template_name='home.html', context={'page_obj': page_obj, 'dates': dates})
        else:
            messages.info(request, f"There are no cars available in your city in the asked time!")
            return render(request=request, template_name='home.html',
                          context={'dates': dates, 'current_user': current_user})
    else:
        cars = Car.objects.all()
        paginator = Paginator(cars, 1)  # Show 25 contacts per page.

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request=request, template_name='home.html', context={'page_obj': page_obj})


def about(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    return render(request=request, template_name='about.html')


@user_passes_test(lambda u: u.is_staff is False)
def search(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    form = SearchForm(request.POST)
    cars = Car.objects.all()
    paginator = Paginator(cars, 1)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    dates = Temporary.objects.filter(user_id=request.user.id).first()
    rented_cars = Rented.objects.filter(rent_till__gte=dates.rent_from).filter(
        rent_from__lte=dates.rent_till).filter(final_status="True").all()
    if form.is_valid():
        searched_cars = form.cleaned_data.get('searched')
        current_user = UserDetails.objects.filter(user_id=request.user.id).first()
        record = CarCompany.objects.filter(company_name__icontains=searched_cars).first()
        if record:
            cars = (Car.objects.filter(company_id=record.id).filter(city_id=current_user.city_id).filter(status="True")
                    .exclude(pk__in=rented_cars).all())
        record = CarCategories.objects.filter(category__icontains=searched_cars).first()
        if record:
            cars = (Car.objects.filter(category_id=record.id).filter(city_id=current_user.city_id).filter(status="True")
                    .exclude(pk__in=rented_cars).all())
        record = CarModels.objects.filter(model_name__icontains=searched_cars).first()
        if record:
            cars = (Car.objects.filter(model_id=record.id).filter(city_id=current_user.city_id).filter(status="True")
                    .exclude(pk__in=rented_cars).all())
        record = City.objects.filter(city__icontains=searched_cars).first()
        if record:
            cars = (Car.objects.filter(city_id=record.id).filter(city_id=current_user.city_id).filter(status="True")
                    .exclude(pk__in=rented_cars).all())
        paginator = Paginator(cars, 1)  # Show 25 contacts per page.

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request=request, template_name='home.html', context={'page_obj': page_obj})
    return render(request=request, template_name='home.html', context={'page_obj': page_obj})


@login_required
def account(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    current_user = request.user

    current_user_details = UserDetails.objects.get(user_id=request.user.id)
    if request.method == "POST":
        form = UpdateAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            current_user_details.city_id = form.cleaned_data.get('city')
            current_user.save()
            current_user_details.save()
            messages.success(request, "Your account has been updated!")
            return redirect('account')
    else:
        form = UpdateAccountForm(instance=request.user, initial={'city': current_user_details.city_id})
    return render(request=request, template_name="form.html",
                  context={"form": form, 'title': 'Account', 'button': 'Update!'})


@login_required
def change_password(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    if request.method == "POST":
        form = ChangePassword(request.POST)
        if form.is_valid():
            current_user = request.user
            if not check_password(form.cleaned_data.get('password'), current_user.password):
                messages.error(request, "Invalid current password!")
                return redirect("change_password")
            else:
                current_user.password = make_password(form.cleaned_data.get('password'))
                current_user.save()
                user = authenticate(username=current_user.username, password=form.cleaned_data.get('password'))
                login(request, user)
                messages.info(request, f"Password successfully changed.")
                return redirect("main-home")
    else:
        form = ChangePassword()
    return render(request=request, template_name="form.html",
                  context={"form": form, 'title': 'Reset Password', 'button': 'Change!'})


@login_required
def logout_request(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main-home")


def login_request(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    if request.user.is_authenticated:
        return redirect('main-home')
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main-home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"form": form})
