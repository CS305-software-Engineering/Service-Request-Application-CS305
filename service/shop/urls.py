from shop.views import *
from django.urls import path, include
from .views import login_attempt,login_otp,register,otp,register_sevice,home,staff_request, user_request, add_request, request_page

urlpatterns = [
    path('', login_attempt, name='login'),
    path('register', register, name='register'),
    path('otp', otp, name='otp'),
    path('login_otp', login_otp, name='login_otp'),
    path('register_service-man',register_sevice,name='register_service'),
    path('home',home, name='home'),
    path('staff_page', staff_request, name='staff_page'),
    path('user_page', user_request, name='user_page'),
    path('request', add_request, name='request'),
    path('request_page', request_page, name='request_page'),
]