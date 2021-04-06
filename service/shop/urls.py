from shop.views import *
from django.urls import path, include
from .views import login_attempt,login_otp,register,otp,register_sevice,home,staff_request, user_request, add_request, feedback_page, thankyou_page

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
    path('feedback_page', feedback_page, name='feedback_page'),
    path('thankyou', thankyou_page, name='thankyou_page'),
]