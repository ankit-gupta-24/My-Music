from django.urls import path
from . import views

urlpatterns = [
    path('',views.loginForm, name='loginForm'),
    path('loginForm/', views.loginForm, name='loginForm'),
    path('registerForm/',views.registerForm, name='registerForm'),
    path('logoutUser/',views.logoutUser, name='logoutUser'),
    path('changePassword/',views.changePassword, name='changePassword'),
    path('changePasswordForm/',views.changePasswordForm, name='changePasswordForm'),
]