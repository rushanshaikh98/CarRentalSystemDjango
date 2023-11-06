from django.urls import path
from . import views

urlpatterns = [
    path('create_cars', views.create_cars, name='create_cars'),
    path('get_car', views.get_car, name='get_car'),
    path('view_car/<car_id>', views.view_car, name='view_car'),
    path('get_delete_car', views.get_delete_car, name='get_delete_car'),
    path('cars_taking_list', views.cars_taking_list, name='cars_taking_list'),
    path('cars_delivery_list', views.cars_delivery_list, name='cars_delivery_list'),
    path('cars_taking_list_late', views.cars_taking_list_late, name='cars_taking_list_late'),
    path('cars_delivery_list_late', views.cars_delivery_list_late, name='cars_delivery_list_late'),
    path('get_maintenance_car', views.get_maintenance_car, name='get_maintenance_car'),
    path('update_car/<car_id>', views.update_car, name='update_car'),
    path('delete_car/<car_id>', views.delete_car, name='delete_car'),
    path('book_car/<car_id>', views.book_car, name='book_car'),
    path('index/<car_id>/<int:days>', views.index, name='index'),
    path('charge/<total_amount>/<int:ids>', views.charge, name='charge'),
    path('confirm_car/<ids>', views.confirm_car, name='confirm_car'),
    path('car_taken/<car_id>', views.car_taken, name='car_taken'),
    path('car_return_review/<car_id>', views.car_return_review, name='car_return_review'),
    path('car_maintenance/<car_id>', views.car_maintenance, name='car_maintenance'),
]