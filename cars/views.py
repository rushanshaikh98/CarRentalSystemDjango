import datetime
import os

import stripe
from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from dotenv import load_dotenv

from .forms import CreateCars, GetCar, UpdateCar, ReturnCar, CarMaintenance

load_dotenv()
Car = apps.get_model('cars', 'Car')
Rented = apps.get_model('cars', 'Rented')
UserDetails = apps.get_model('users', 'UserDetails')
Temporary = apps.get_model('users', 'Temporary')
Maintenance = apps.get_model('cars', 'Maintenance')
stripe.api_key = os.environ.get('stripe_sk')


# stripe.secret_key = ''

# Create your views here.
@user_passes_test(lambda u: u.is_staff)
def create_cars(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    if request.method == "POST":
        form = CreateCars(request.POST)
        if form.is_valid():
            car = Car(number_plate=form.cleaned_data.get('number_plate').replace(" ", "").upper(),
                      company_id=form.cleaned_data.get('company'), category_id=form.cleaned_data.get('category'),
                      model_id=form.cleaned_data.get('model'),
                      color=form.cleaned_data.get('color').replace(" ", "").upper(),
                      mileage=form.cleaned_data.get('mileage'), ppd=form.cleaned_data.get('ppd'),
                      min_rent=form.cleaned_data.get('min_rent'), city_id=form.cleaned_data.get('city'),
                      deposit=form.cleaned_data.get('deposit'))
            car.save()
            messages.success(request, f'Car has been added successfully!')
            return redirect('main-home')
    else:
        form = CreateCars()
    return render(request, 'form.html', {'form': form, 'title': 'Create Car', 'button': 'Create!'})


@user_passes_test(lambda u: u.is_staff)
def get_car(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    if request.method == "POST":
        form = GetCar(request.POST)
        if form.is_valid():
            car = Car.objects.filter(
                number_plate=form.cleaned_data.get('number_plate').replace(" ", "").upper()).first()
            if car:
                return redirect('update_car', car_id=car.id)
            else:
                messages.error(request, 'Car with this number plate does not exist!')
                return redirect('main-home')
    else:
        form = GetCar()
    return render(request, 'form.html', {'form': form, 'title': 'Get Car', 'button': 'Get!'})


@user_passes_test(lambda u: u.is_staff)
def update_car(request, car_id):
    """Method to update a car which can only be accessed by the admin. If the request method is get, a form is called
    which already has the current details of that car and the user can update that details and upon the validation of
    the form, the car is updated.
    -----------------------------
    Returns: The success flash message and redirects to the home page"""

    car = Car.objects.filter(id=car_id).first()

    if request.method == "POST":
        form = UpdateCar(request.POST)
        if form.is_valid():
            car.color = form.cleaned_data.get('color').replace(" ", "").upper()
            car.mileage = form.cleaned_data.get('mileage')
            car.ppd = form.cleaned_data.get('ppd')
            car.min_rent = form.cleaned_data.get('min_rent')
            car.deposit = form.cleaned_data.get('deposit')
            car.city_id = form.cleaned_data.get('city')
            car.status = form.cleaned_data.get('status')
            car.save()
            messages.success(request, ' Car has been updated successfully!')
            return redirect('main-home')
    else:
        form = UpdateCar(initial={'city': car.city_id, 'status': car.status, 'color': car.color, 'mileage': car.mileage,
                                  'ppd': car.ppd, 'min_rent': car.min_rent, 'deposit': car.deposit})
    return render(request, 'form.html', {'form': form, 'title': 'Update Car', 'button': 'Update!'})


@user_passes_test(lambda u: u.is_staff)
def get_delete_car(request):
    """Method to get the car by the admin in order to delete that car. If the request method is get, a form is called
    to take car id and upon the validation of the form, it returns that car.
    -----------------------------
    Returns: The car details with a delete button."""

    if request.method == "POST":
        form = GetCar(request.POST)
        if form.is_valid():
            car = Car.objects.filter(
                number_plate=form.cleaned_data.get('number_plate').replace(" ", "").upper()).first()
            if car:
                return redirect('delete_car', car_id=car.id)
            else:
                messages.error(request, 'Car with this number plate does not exist!')
                return redirect('main-home')
    else:
        form = GetCar()
    return render(request, 'form.html', {'form': form, 'title': 'Get Car', 'button': 'Get!'})


@user_passes_test(lambda u: u.is_staff)
def delete_car(request, car_id):
    """Method to delete a car which can only be accessed by the admin. The car will be deleted from the database if no
    further booking of that car are there in the database else it will not be deleted.
    -----------------------------
    Returns: The success flash message and redirects to the home page"""

    record = Rented.objects.filter(car_id=car_id).filter(final_status="True").first()
    if record:
        if record.rent_till > datetime.date.today():
            messages.info(request, "This car cannot be deleted as it is booked by a someone!")
        else:
            Car.objects.filter(id=car_id).delete()
            messages.success(request, "Car deleted successfully!")
    else:
        Car.objects.filter(id=car_id).delete()
        messages.success(request, "Car deleted successfully!")
    return redirect('main-home')


def view_car(request, car_id):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    car = Car.objects.filter(id=car_id).first()
    return render(request, 'view_car.html', {'car': car})


@user_passes_test(lambda u: u.is_staff)
def cars_taking_list(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    user_details = UserDetails.objects.filter(user_id=request.user.id).first()
    orders = Rented.objects.filter(city_taken_id=user_details.city_id).filter(final_status="True").filter(
        rent_from=datetime.date.today()).filter(car_taken=False).all()
    if orders:
        paginator = Paginator(orders, 1)  # Show 25 contacts per page.

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, 'cars_taking.html', {'page_obj': page_obj})
    else:
        messages.info(request, 'There are no booking for today!')
        return redirect('main-home')


@user_passes_test(lambda u: u.is_staff)
def car_taken(request, car_id):
    """Method which can only be accessed by the admin for entering that the car is taken by the user in the admin.
    -----------------------------
    Returns: Enter the data that the car is taken by the user and redirects to the home page"""

    record = Rented.objects.filter(id=car_id).first()
    record.car_taken = True
    record.save()
    messages.success(request, 'Car is Taken!')
    return redirect('main-home')


@user_passes_test(lambda u: u.is_staff)
def cars_delivery_list(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    user_details = UserDetails.objects.filter(user_id=request.user.id).first()
    orders = Rented.objects.filter(city_delivery_id=user_details.city_id).filter(final_status="True").filter(
        rent_till=datetime.date.today()).filter(car_taken=True).filter(car_delivery=False).all()
    if orders:
        paginator = Paginator(orders, 1)  # Show 25 contacts per page.

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, 'cars_delivery.html', {'page_obj': page_obj})
    else:
        messages.info(request, 'There are no car returns for today')
        return redirect('main-home')


@user_passes_test(lambda u: u.is_staff)
def cars_taking_list_late(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    user_details = UserDetails.objects.filter(user_id=request.user.id).first()
    orders = Rented.objects.filter(city_taken_id=user_details.city_id).filter(final_status="True").filter(
        rent_from__lt=datetime.date.today()).filter(rent_till__gt=datetime.date.today()).filter(car_taken=False).all()
    if orders:
        paginator = Paginator(orders, 1)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, 'cars_taking.html', {'page_obj': page_obj})
    else:
        messages.info(request, 'There are no previous bookings which are pending!')
        return redirect('main-home')


@user_passes_test(lambda u: u.is_staff)
def cars_delivery_list_late(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    user_details = UserDetails.objects.filter(user_id=request.user.id).first()
    orders = Rented.objects.filter(city_delivery_id=user_details.city_id).filter(final_status="True").filter(
        rent_till__lt=datetime.date.today()).filter(car_taken=True).filter(car_delivery=False).all()
    if orders:
        paginator = Paginator(orders, 1)  # Show 25 contacts per page.

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, 'cars_delivery.html', {'page_obj': page_obj})
    else:
        messages.info(request, 'There are no car returns for previous days!')
        return redirect('main-home')


@user_passes_test(lambda u: u.is_staff)
def car_return_review(request, car_id):
    """Method which can only be accessed by the admin for entering the details of the car when the car is returned.
    If the request method is get, a form is called which takes all the data from the admin and upon the validation of
    that form, the data is entered in the database and user is charged fine if any.
    -----------------------------
    Returns: The success flash message and redirects to the home page"""

    if request.method == "POST":
        form = ReturnCar(request.POST)
        if form.is_valid():
            record = Rented.objects.filter(id=car_id).first()
            record.said_date = form.cleaned_data.get('said_date')
            record.said_time = form.cleaned_data.get('said_time')
            record.proper_condition = form.cleaned_data.get('proper_condition')
            record.description = form.cleaned_data.get('description')
            record.fine = form.cleaned_data.get('fine')
            if form.cleaned_data.get('fine') > 0:
                user = User.objects.filter(id=record.user_id).first()
                user_details = UserDetails.objects.filter(user_id=user.id).first()
                user_details.fine_pending = True
                user_details.save()
            record.car_delivery = True
            record.save()
            messages.success(request, 'Car reviewed!')
            return redirect('main-home')
    else:
        form = ReturnCar()
    return render(request, 'form.html', {'form': form, 'title': 'Return Car Form', 'button': 'Add Details!'})


@user_passes_test(lambda u: u.is_staff)
def get_maintenance_car(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    if request.method == "POST":
        form = GetCar(request.POST)
        if form.is_valid():
            car = Car.objects.filter(
                number_plate=form.cleaned_data.get('number_plate').replace(" ", "").upper()).first()
            if car:
                return redirect('car_maintenance', car_id=car.id)
            else:
                messages.error(request, 'Car with this number plate does not exist!')
                return redirect('main-home')
    else:
        form = GetCar()
    return render(request, 'form.html', {'form': form, 'title': 'Get Car', 'button': 'Get!'})


@user_passes_test(lambda u: u.is_staff is False)
def book_car(request, car_id):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    user_details = UserDetails.objects.filter(user_id=request.user.id).first()
    if not user_details.fine_pending:
        user = Temporary.objects.filter(user_id=request.user.id).first()
        rented_cars = Rented.objects.filter(rent_till__gte=user.rent_from).filter(rent_from__lte=user.rent_till).filter(
            car_id=car_id).filter(final_status="True").all()
        if rented_cars:
            messages.warning(request, "Sorry! This car is already booked!")
            return redirect('main-home')
        record = Rented.objects.filter(rent_till__gte=user.rent_from).filter(rent_from__lte=user.rent_till).filter(
            user_id=request.user.id).filter(final_status="True").all()
        if record:
            messages.warning(request, "Sorry! You already have a booking for this time period and you can only "
                                      "book a single car at a given time!")
            return redirect('main-home')
        else:
            car = Car.objects.filter(id=car_id).first()
            dates = Temporary.objects.filter(user_id=request.user.id).first()
            days = int(str(dates.rent_till - dates.rent_from).split(" ")[0])
            rent_from = str(dates.rent_from).split(" ")[0]
            rent_till = str(dates.rent_till).split(" ")[0]
            if days <= 1:
                rent_amount = car.min_rent
                total_amount = car.min_rent + car.deposit
            else:
                rent_amount = days * car.ppd
                total_amount = (days * car.ppd) + car.deposit

            return render(request, 'payment.html',
                          {'car': car, 'days': days, 'rent_from': rent_from, 'rent_till': rent_till, 'dates': dates,
                           'rent_amount': rent_amount, 'total_amount': total_amount})
    else:
        messages.warning("You first need the to pay your previous fine to book a car!", "warning")
        return redirect('main-home')


@user_passes_test(lambda u: u.is_staff is False)
def index(request, car_id, days):
    """Method to call the payment page for paying the Rent of the car by clicked on the book car button.
    -----------------------------
    Returns: The payment page with a button to pay the required amount of money"""

    car = Car.objects.filter(id=car_id).first()
    total_amount = (int(days) * car.ppd) + car.deposit
    return render(request, 'index.html',
                  {'total_amount': total_amount * 100, 'key': os.environ.get('stripe_pk'), 'ids': car.id})


@user_passes_test(lambda u: u.is_staff is False)
def charge(request, total_amount, ids):
    """Method for paying the amount of money, a user need to pay for booking a car.
    -----------------------------
    Returns: The payment page entering all the details to pay the amount required"""

    customer = stripe.Customer.create(email=request.user.email, source=request.POST.get('stripeToken'))

    stripe.PaymentIntent.create(customer=customer.id, amount=int(total_amount), payment_method='pm_card_visa',
                                currency='INR', description='Rent Car')

    return redirect('confirm_car', ids=ids)


@user_passes_test(lambda u: u.is_staff is False)
def confirm_car(request, ids):
    """Method to confirm the booking of the user in the database only after he has completed his payment.
    -----------------------------
    Returns: The success flash message and redirects to the home page"""

    user_details = UserDetails.objects.filter(user_id=request.user.id).first()
    dates = Temporary.objects.filter(user_id=request.user.id).first()
    rent = Rented(car_id=ids, user_id=request.user.id, booking_time=datetime.datetime.now(), rent_from=dates.rent_from,
                  rent_till=dates.rent_till, city_taken_id=user_details.city_id, city_delivery_id=dates.city_id)

    rent.save()
    messages.success(request, "The car has been booked successfully!")
    return redirect('main-home')


@user_passes_test(lambda u: u.is_staff)
def car_maintenance(request, car_id):
    """Method to enter the car maintenance for a car if required which can only be accessed by an admin.
    If the request method is get, a form is called to enter the car details and upon the validation of that form,
    the details are added to the database and also the car is made unavailable for booking.
    -----------------------------
    Returns: The success flash message and redirects to the home page"""

    car = Car.objects.filter(id=car_id).first()
    if request.method == "POST":
        form = CarMaintenance(request.POST)
        if form.is_valid():
            record = Maintenance(car_id=car_id, date=datetime.datetime.utcnow(),
                                 description=form.cleaned_data.get('description'), user_id=request.user.id)
            record.save()
            car.status = False
            car.save()
            messages.success(request, 'Car successfully added to maintenance!')
            return redirect('main-home')
    else:
        form = CarMaintenance()
    return render(request, 'form.html', {'form': form, 'title': 'Car Maintenance', 'button': 'Add!'})
