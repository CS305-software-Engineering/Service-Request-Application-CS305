from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from shop.models import EndUser,serviceman,Request

import random
import http.client
from django.http import HttpResponse

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
        print(user)
        service_man = serviceman.objects.filter(phone = phone).first()
        print(service_man)
        if user is None and service_man is not None:
            otp = str(random.randint(1000, 9999))
            service_man.otp = otp
            service_man.save()
            send_otp(phone, otp)
            request.session['phone'] = phone
            request.session['type'] = 2
            return redirect('login_otp')

        elif user is not None and service_man is None:
            otp = str(random.randint(1000, 9999))
            user.otp = otp
            user.save()
            send_otp(phone, otp)
            request.session['phone'] = phone
            request.session['type'] = 1
            return redirect('login_otp')
        else:
            context = {'message': 'User not found', 'class': 'danger'}
            return render(request, 'accounts/login.html', context)

        # otp = str(random.randint(1000, 9999))
        # user.otp = otp
        # user.save()
        # send_otp(phone, otp)

        # request.session['phone'] = phone
        # return redirect('login_otp')

    return render(request, 'accounts/login.html')

def login_otp(request):
    phone = request.session['phone']
    type_ = request.session['type']
    context = {'phone': phone}

    if request.method == "POST":
        otp = request.POST.get('otp')
        if type_==1:
            user = EndUser.objects.filter(phone=phone).first()

            if otp == user.otp:
                user = User.objects.get(id = user.user.id)
                login(request, user)
                return redirect('home')
            else:
                context = {'message': 'Wrong OTP', 'class': 'danger', 'phone': phone}
                return render(request, 'accounts/login_otp.html', context)

        else:
            service_man = serviceman.objects.filter(phone=phone).first()

            if otp == service_man.otp:
                user = User.objects.get(id = service_man.user.id)
                login(request, user)
                return redirect('home')
            else:
                context = {'message': 'Wrong OTP', 'class': 'danger', 'phone': phone}
                return render(request, 'accounts/login_otp.html', context)


    return render(request, 'accounts/login_otp.html', context)

def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        check_user = User.objects.filter(email = email).first()
        check_enduser = EndUser.objects.filter(phone = phone).first()

        if check_user or check_enduser:
            context = {'message': 'User already exists', 'class': 'danger'}
            return render(request, 'accounts/register.html', context)

        user = User(username = phone, email = email, first_name = name)
        user.save()

        otp = str(random.randint(1000, 9999))
        enduser = EndUser(user = user, phone = phone, otp = otp)
        enduser.save()

        send_otp(phone, otp)
        request.session['phone'] = phone
        request.session['type'] = 1
        return redirect('otp')

    return render(request, 'accounts/register.html')

def otp(request):
    phone = request.session["phone"]
    type_ = request.session['type']
    context = {'phone' : phone,'type':type_}

    if request.method == "POST":
        otp = request.POST.get('otp')
        if type_== 1:
            enduser = EndUser.objects.filter(phone = phone).first()

            if otp == enduser.otp:
                user = User.objects.get(id = enduser.user.id)
                login(request, user)
                return redirect('home')
            else:
                context = {"message": "Wrong OTP", "class": "danger", "phone": phone,"type":type_}
                return render(request, "accounts/otp.html", context)
        else:
            service_man = serviceman.objects.filter(phone = phone).first()

            if otp == service_man.otp:
                user = User.objects.get(id = service_man.user.id)
                login(request, user)
                return redirect('home')
            else:
                context = {"message": "Wrong OTP", "class": "danger", "phone": phone,"type":type_}
                return render(request, "accounts/otp.html", context)

    return render(request, "accounts/otp.html", context) 

def register_sevice(request):
    if request.method == "POST":
        email = request.POST.get('email')
        company_name = request.POST.get('company_name')
        phone = request.POST.get('phone')
        is_plumber=request.POST.get('is_plumber')=="on"
        is_electrician=request.POST.get('is_electrician')=="on"
        is_mechanic=request.POST.get('is_mechanic')=="on"
        other_services=request.POST.get('other_services')
        #print(is_plumber)
        check_user = User.objects.filter(email = email).first()
        check_serviceman = serviceman.objects.filter(phone = phone).first()

        if check_user or check_serviceman:
            context = {'message': 'User already exists', 'class': 'danger'}
            return render(request, 'accounts/register_sm.html', context)

        user = User(username = phone, email = email, first_name = company_name)
        user.save()

        otp = str(random.randint(1000, 9999))
        service_man = serviceman(user = user, phone = phone, otp = otp,is_plumber=is_plumber,is_electrician=is_electrician,is_mechanic=is_mechanic,other_services=other_services,company_name=company_name)
        service_man.save()

        send_otp(phone, otp)
        request.session['phone'] = phone
        request.session['type'] = 2
        return redirect('otp')

    return render(request, 'accounts/register_sm.html')

def home(request):
    return render(request, 'shop/home.html')


def user_request(request):
    current_user = request.user
    service_requests = Request.objects.filter(customer_id = current_user.id)
    context = {
        'requests' : service_requests
    }

    return render(request, 'shop/user_page.html', context)

def request_page(request):
    if request.method == 'POST':
        request_id = request.POST['request']
        service_request = Request.objects.filter(requestid = request_id).first()
        context = {
            'service_request' : service_request
        }

        return render(request, 'shop/request_page.html', context)

def add_request(request):
    def classicication(image):
        ## Code for image classification
        image_type = "The output" ## Output
        return image_type


    if request.method == 'POST':
        requestid = request.POST.get('requestid')
        accepted = request.POST.get('accepted')
        customer_id = request.POST.get('customer_id')
        serviceman_id = request.POST.get('serviceman_id')
        cost = request.POST.get('cost')
        ispaid = request.POST.get('is_paid')
        department = request.POST.get('department')
        completed = request.POST.get('completed')
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')
        given_request = Request(requestid = requestid, 
                                accepted = accepted    ,
                                customer_id = customer_id,
                                serviceman_id = serviceman_id,
                                cost = cost,
                                ispaid = ispaid,
                                department = department,
                                completed = completed,
                                rating = rating,
                                feedback = feedback
                                )
        given_request.save()
        context = {"message": "Successful", "class": "OK","status":201}
        return render(request, "shop/new_request.html", context)

def staff_request(request):    
    if request.method == 'GET':
        all_request = Request.objects.all()
        context = {"requests": all_request}
        return render(request,"shop/staff_page.html",context)
    if request.method == 'POST':
        requestid = request.POST.get('requestid')
        accepted = request.POST.get('accepted')
        customer_id = request.POST.get('customer_id')
        serviceman_id = request.POST.get('serviceman_id')
        cost = request.POST.get('cost')
        ispaid = request.POST.get('is_paid')
        department = request.POST.get('department')
        completed = request.POST.get('completed')
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')
        given_request = Request(requestid = requestid, 
                                accepted = accepted    ,
                                customer_id = customer_id,
                                serviceman_id = serviceman_id,
                                cost = cost,
                                ispaid = ispaid,
                                department = department,
                                completed = completed,
                                rating = rating,
                                feedback = feedback
                                )
        given_request.save()
        context = {"message": "Successful", "class": "OK","status":201}
        # context = {"message": "No request found", "class": "danger","status":404}
        return render(request, "shop/staff_page.html", context)


