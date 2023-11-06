import datetime
import os

import stripe
from django.apps import apps
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from dotenv import load_dotenv

from .forms import RegistrationForm, TakingDates, ApprovalForm

load_dotenv()

Temporary = apps.get_model('users', 'Temporary')
Rented = apps.get_model('cars', 'Rented')
UserVerification = apps.get_model('users', 'UserVerification')
UserDetails = apps.get_model('users', 'UserDetails')


# Create your views here.
@user_passes_test(lambda u: u.is_staff)
def display_users_list(request):
    """Method to display the list of all the users which have currently applied for the user verification which can only
    be accessed by an admin.
    -----------------------------
    Returns: The users list if users are there for verification else return an info flash message
    and redirects to home"""

    users_list = UserVerification.objects.filter(approval='').select_related('user').all()
    if users_list:
        return render(request=request, template_name="verify_users_list.html", context={'users_list': users_list})
    else:
        messages.error(request, "There are no users to verify!")
        return redirect('main-home')


@user_passes_test(lambda u: u.is_staff is False)
def taking_dates(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    if request.method == "POST":
        form = TakingDates(request.POST)
        if form.is_valid():
            rent_from = form.cleaned_data.get('rent_from')
            rent_till = form.cleaned_data.get('rent_till')
            city_delivery = form.cleaned_data.get('city')
            record = Temporary.objects.filter(user_id=request.user.id).first()
            if record:
                record.rent_from = rent_from
                record.rent_till = rent_till
                record.city_id = city_delivery
                record.save()
            else:
                new_record = Temporary(user_id=request.user.id, rent_from=rent_from, rent_till=rent_till,
                                       city_id=city_delivery)
                new_record.save()

            return redirect('main-home')
    else:
        form = TakingDates()
    return render(request=request, template_name="form.html",
                  context={"form": form, 'title': 'Enter Data', 'button': 'Update!'})


@user_passes_test(lambda u: u.is_staff is False)
def apply_for_verification(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""

    records = UserVerification.objects.filter(user_id=request.user.id).order_by("-id").all()
    if records:
        if records[0].approval == "":
            messages.info(request, "Please wait for the previous request to be responded!")
            return redirect('main-home')
        if records[0].approval == "true":
            messages.info(request, "Your account is already verified!")
            return redirect('main-home')
    if request.method == "POST":
        form = ApprovalForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data.get('id_proof'):
                row = UserVerification(user_id=request.user.id, id_proof=form.cleaned_data.get('id_proof'), approval="",
                                       date=datetime.date.today())
                row.save()
            messages.success(request, 'Your documents are submitted successfully! Please wait for the approval.')
            return redirect('main-home')
    else:
        form = ApprovalForm()
    return render(request=request, template_name="form.html",
                  context={"form": form, 'title': 'Apply for Verification', 'button': 'Apply!'})


@user_passes_test(lambda u: u.is_staff is False)
def bookings(request):
    """Method to display all the booking he has done through his website with all the status which can only be accessed
    by an authenticated user.
    -----------------------------
    Returns: The bookings list if the user has bookings else returns info flash message and redirects to home page"""

    orders = Rented.objects.filter(user_id=request.user.id).order_by('-booking_time').all()
    current_date = datetime.date.today()
    if orders:
        paginator = Paginator(orders, 1)  # Show 25 contacts per page.

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, 'orders.html', {'page_obj': page_obj, 'current_date': current_date})
    else:
        messages.info(request, "You dont have any bookings!")
        return redirect('main-home')


def register(request):
    """Method for displaying the home page of the website to any type of user. It detects the user by his role
    and redirects to user according to his requirements.
    -----------------------------
    Returns: The home page according to the requirements of the user"""
    if request.user.is_authenticated:
        return redirect('main-home')
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_details = UserDetails(user_id=user.id, city_id=form.cleaned_data.get('city'))
            user_details.save()
            login(request, user)
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('main-home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@user_passes_test(lambda u: u.is_staff is False)
def cancel_booking(request, booking_id):
    """Method to cancel the booking for a user. This method is called when the user clicks the cancel button which is
    clicked by the user.
    -----------------------------
    Returns: The success flash message and redirects again to the bookings page"""

    record = Rented.objects.filter(id=booking_id).first()
    if record.rent_from > datetime.date.today():
        record.final_status = "False"
        record.save()
        messages.success(request, "Your booking has been cancelled!")
        return redirect('bookings')
    else:
        messages.warning(request, "You cannot cancel this booking now!")
        return redirect('main-home')


@user_passes_test(lambda u: u.is_staff is False)
def fine_index(request, booking_id, total_amount):
    """Method to call the payment page for paying the fine of the car by clicked on the pay fine button.
    -----------------------------
    Returns: The payment page with a button to pay the required amount of money"""

    return render(request, 'fine_index.html',
                  {'total_amount': int(total_amount) * 100, 'key': os.environ.get('stripe_pk'),
                   'booking_id': booking_id})


@user_passes_test(lambda u: u.is_staff is False)
def fine_charge(request, booking_id, total_amount):
    """Method for paying the amount of money, a user need to pay for booking a car.
    -----------------------------
    Returns: The payment page entering all the details to pay the amount required"""

    customer = stripe.Customer.create(email=request.user.email, source=request.POST.get('stripeToken'))

    stripe.PaymentIntent.create(customer=customer.id, amount=int(total_amount), payment_method='pm_card_visa',
                                currency='INR', description='Pay Fine')

    return redirect('pay_fine', booking_id=booking_id)


@user_passes_test(lambda u: u.is_staff is False)
def pay_fine(request, booking_id):
    """Method to pay fine for all the user. It updates all the details in the database when the fine
    is paid by the user.
    -----------------------------
    Returns: The success flash message and redirects to home page"""

    record = Rented.objects.filter(id=booking_id).first()
    user = UserDetails.objects.filter(user_id=record.user_id).first()
    record.fine_paid = True
    user.fine_pending = False
    record.save()
    messages.success(request, 'You have successfully paid the fine amount!')
    return redirect('main-home')
