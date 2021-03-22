from shop.views import *
from django.urls import path, include

urlpatterns = [
    path('', login_attempt, name='login'),
    path('register', register, name='register'),
    path('otp', otp, name='otp'),
    path('login_otp', login_otp, name='login_otp'),
]