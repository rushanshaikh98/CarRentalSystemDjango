from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('about', views.about, name='about'),
    path('search', views.search, name='search'),
    path('account', views.account, name='account'),
    path('change_password', views.change_password, name='change_password'),
    path('logout', views.logout_request, name='logout'),
    path('login', views.login_request, name='login'),
    path('password_reset',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html'
         ),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ),
         name='password_reset_complete'),
]