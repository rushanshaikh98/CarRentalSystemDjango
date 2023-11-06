from django.urls import path
from . import views

urlpatterns = [
    path('display_users_list', views.display_users_list, name='display_users_list'),
    path('taking_dates', views.taking_dates, name='taking_dates'),
    path('apply_for_verification', views.apply_for_verification, name='apply_for_verification'),
    path('bookings', views.bookings, name='bookings'),
    path('register', views.register, name='register'),
    path('apply_for_verification', views.apply_for_verification, name='apply_for_verification'),
    path('cancel_booking/<booking_id>', views.cancel_booking, name='cancel_booking'),
    path('fine_index/<booking_id>/<total_amount>', views.fine_index, name='fine_index'),
    path('fine_charge/<booking_id>/<total_amount>', views.fine_charge, name='fine_charge'),
    path('pay_fine/<booking_id>', views.pay_fine, name='pay_fine'),
]