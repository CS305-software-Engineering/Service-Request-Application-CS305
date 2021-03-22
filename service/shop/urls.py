from shop.views import *
from django.urls import path, include
from .views import login_attempt,login_otp,register,otp,register_sevice,home

urlpatterns = [
    path('', login_attempt, name='login'),
    path('register', register, name='register'),
    path('otp', otp, name='otp'),
    path('login_otp', login_otp, name='login_otp'),
    path('register_service-man',register_sevice,name='register_service'),
    path('home',home, name='home'),
]