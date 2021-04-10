from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from clarifai.rest import ClarifaiApp
from PIL import Image
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from shop.models import EndUser,serviceman,Request

import random
import http.client
from django.http import HttpResponse

try:
    app = ClarifaiApp(api_key="")
except:
    print("Please provide a valid API KEY for Image classification Clarifai API")
    exit()

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

def feedback_page(request):
    if request.method == 'POST':
        request_id = request.POST['request']
        request.session['request_id'] = request_id
        service_request = Request.objects.filter(requestid = request_id).first()
        context = {
            'service_request' : service_request
        }

        return render(request, 'shop/feedback_page.html', context)

def thankyou_page(request):
    if request.method == "POST":
        request_id = request.session['request_id']
        service_request = Request.objects.filter(requestid = request_id).first()

        service_request.feedback = request.POST['feedback']
        service_request.rating = request.POST['rating']
        service_request.save()
        
        context = {"message": "Successful", "class": "OK","status":201}

        return render(request, 'shop/thankyou_page.html', context)


######## This function takes a public url of the image and sends the predictions ################
def get_tags_from_url(image_url):
    response_data = app.tag_urls([image_url])
    tags = []
    for concept in response_data['outputs'][0]['data']['concepts']:
        tags.append(concept['name'])
    return tags

#### this can take a path of a local image file as input, uses OS library and sends predictions ##########################
def get_tags_from_path(img):
    # print(type(img))
    response_data = app.tag_files([img])
    tags = []
    for concept in response_data['outputs'][0]['data']['concepts']:
        tags.append(concept['name'])
    return tags



path = 'F:/Pythons/resources/iron1.jpg'
faucet_url1 = 'https://www.aquantindia.com/wp-content/uploads/2020/04/Faucets-in-Chrome-Finish.jpg'
# file = Image.open('F:/Pythons/resources/iron1.jpg')
# file.show()

def classification(image_path):
    ## Code for image classification
    validate = URLValidator()
    try: 
        validate(image_path)
        print("is a URL =>", image_path)
        try:
            tags = get_tags_from_url(image_path)
        
        except:
            return "invalid URL of the image file, kindly enter exact path of the image file or image url"
    except ValidationError as e:
        print("is not a url =>",image_path)
        try:
            tags = get_tags_from_path(image_path)
            
        except:
            return "invalid PATH of the image file, kindly enter exact path of the image file or image url"

    plumber_set = ['faucet','pipes','pipe','shower','water']
    electrical_set = ['electrical','electronics','power','appliance']  
    score_plumber = 0
    score_electrical =0
    for tag in tags:
        if(tag in plumber_set):
            score_plumber+=1
        if(tag in electrical_set):
            score_electrical+=1
    
    if(max(score_electrical,score_plumber)==0):
        return "something went wrong, could not predict the department"
    else:
        if(score_plumber>=score_electrical):
            return "plumber"
        else:
            return "electrical"

def add_request(request):
    if request.method == 'GET':
        all_request = Request.objects.all()
        context = {"requests": all_request}
        return render(request,"shop/add_request.html",context)
    if request.method == 'POST':
#         requestid = request.POST.get('requestid')
        # accepted = request.POST.get('accepted')
        # customer_id = request.POST.get('customer_id')
        typee = request.session.get('type')
        image = request.POST.get("img")
        dept_drop = request.POST.get("dropDownDept")
        car = request.POST.get("carSelected")
        print("type => ",typee)
        print("image=>",image)
        print("dept_drop =>", dept_drop)
        print("car =>",car)
        dept = "default_dept"
        # dept = classification(image)
        # print("department predicted =>",department)
#         serviceman_id = request.POST.get('serviceman_id')
#         cost = request.POST.get('cost')
#         ispaid = request.POST.get('is_paid')
        department = request.POST.get('department',"_")
        # completed = request.POST.get('completed')
        # rating = request.POST.get('rating')
        # feedback = request.POST.get('feedback')
        given_request = Request(
                                # accepted = accepted    ,
                                department = department,
                                # completed = completed,
                                # rating = rating,
                                # feedback = feedback
                                )
        given_request.save()
        context = {"message": "Successful", "class": "OK","status":201}
        return render(request, "shop/add_request.html", context)

def staff_request(request):    
    if request.method == 'GET':
        all_request = Request.objects.all()
        context = {"requests": all_request}
        return render(request,"shop/staff_page.html",context)
    if request.method == 'POST':
#         requestid = request.POST.get('requestid')
        accepted = request.POST.get('accepted')
#         customer_id = request.POST.get('customer_id')
#         serviceman_id = request.POST.get('serviceman_id')
        cost = request.POST.get('cost')
#         ispaid = request.POST.get('is_paid')
        department = request.POST.get('department')
        completed = request.POST.get('completed')
#         rating = request.POST.get('rating')
#         feedback = request.POST.get('feedback')
        given_request = Request( 
                                accepted = accepted    ,
                                cost = cost,
                                department = department,
                                completed = completed,
                               
                                )
        given_request.save()
        context = {"message": "Successful", "class": "OK","status":201}
        # context = {"message": "No request found", "class": "danger","status":404}
        return render(request, "shop/staff_page.html", context)


