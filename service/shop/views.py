from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from shop.models import EndUser

import random
import http.client

# Create your views here.
def send_otp(mobile, otp):
    # conn = http.client.HTTPSConnection("api.msg91.com")
    # authkey = settings.AUTH_KEY
    # headers = {'content-type': "application/json"}

    # url = "http://control.msg91.com/api/sendotp.php?"
    # url += "otp="+ otp 
    # url += "&message=" + "Your otp is " + otp 
    # url += "&mobile=" + mobile 
    # url += "&authkey=" + authkey + "&country=91"

    # conn.request("GET", url, headers=headers)
    # response = conn.getresponse()
    # data = response.read()
    print("Mobile: {mobile} OTP: {otp}".format(mobile=mobile, otp=otp))
    return None

def login_attempt(request):
    if request.method == "POST":
        phone = request.POST.get('phone')

        user = EndUser.objects.filter(phone=phone).first()
        if user is None:
            context = {'message': 'User not found', 'class': 'danger'}
            return render(request, 'shop/login.html', context)

        otp = str(random.randint(1000, 9999))
        user.otp = otp
        user.save()
        send_otp(phone, otp)

        request.session['phone'] = phone
        return redirect('login_otp')

    return render(request, 'shop/login.html')

def login_otp(request):
    phone = request.session['phone']
    context = {'phone': phone}

    if request.method == "POST":
        otp = request.POST.get('otp')
        user = EndUser.objects.filter(phone=phone).first()

        if otp == user.otp:
            user = User.objects.get(id = user.user.id)
            login(request, user)
            return redirect('https://www.google.com')

        else:
            context = {'message': 'Wrong OTP', 'class': 'danger', 'phone': phone}
            return render(request, 'shop/login_otp.html', context)

    return render(request, 'shop/login_otp.html', context)

def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        check_user = User.objects.filter(email = email).first()
        check_enduser = EndUser.objects.filter(phone = phone).first()

        if check_user or check_enduser:
            context = {'message': 'User already exists', 'class': 'danger'}
            return render(request, 'shop/register.html', context)

        user = User(username = phone, email = email, first_name = name)
        user.save()

        otp = str(random.randint(1000, 9999))
        enduser = EndUser(user = user, phone = phone, otp = otp)
        enduser.save()

        send_otp(phone, otp)
        request.session['phone'] = phone
        return redirect('otp')

    return render(request, 'shop/register.html')

def otp(request):
    phone = request.session["phone"]
    context = {'phone' : phone}

    if request.method == "POST":
        otp = request.POST.get('otp')
        enduser = EndUser.objects.filter(phone = phone).first()

        if otp == enduser.otp:
            return redirect("https://www.google.com")
        else:
            context = {"message": "Wrong OTP", "class": "danger", "phone": phone}
            return render(request, "shop/otp.html", context)

    return render(request, "shop/otp.html", context) 