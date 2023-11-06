from django.urls import path
from . import views

urlpatterns = [
    path('create_admins', views.create_admins, name='create_admins'),
    path('admin_list', views.admin_list, name='admin_list'),
    path('add_city', views.add_city, name='add_city'),
    path('update_city', views.update_city, name='update_city'),
    path('delete_city', views.delete_city, name='delete_city'),
    path('add_company', views.add_company, name='add_company'),
    path('update_company', views.update_company, name='update_company'),
    path('delete_company', views.delete_company, name='delete_company'),
    path('add_category', views.add_category, name='add_category'),
    path('update_category', views.update_category, name='update_category'),
    path('delete_category', views.delete_category, name='delete_category'),
    path('add_model', views.add_model, name='add_model'),
    path('update_model', views.update_model, name='update_model'),
    path('delete_model', views.delete_model, name='delete_model'),
    path('delete_admin/<user_id>', views.delete_admin, name='delete_admin'),
    path('view_image/<img>', views.view_image, name='view_image'),
    path('accept_user/<user_id>', views.accept_user, name='accept_user'),
    path('reject_user/<user_id>', views.reject_user, name='reject_user'),
]