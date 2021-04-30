from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from clarifai.rest import ClarifaiApp
from PIL import Image
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from dotenv import load_dotenv
import os
import datetime
from service.settings import MEDIA_ROOT
from dateutil.parser import parse
load_dotenv()

from .models import EndUser,serviceman,Request,Appointments

import random
import http.client
from django.http import HttpResponse

try:
    keykey = os.environ.get('CLARIFAI_API_KEY')
    app = ClarifaiApp(api_key=keykey)
except:
    print("Please provide a valid API KEY for Image classification Clarifai API")
    #exit()

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
        password = request.POST.get('password')

        end_user = EndUser.objects.filter(phone=phone).first()
        print(end_user)
        service_man = serviceman.objects.filter(phone = phone).first()
        print(service_man)

        if end_user is None and service_man is not None: # is a service_man
            user = authenticate(request, username=phone, password=password)
            print(user)
            if user is not None:
                login(request, user)
                request.session['phone'] = phone
                request.session['type'] = 2
                return redirect('home')
            else:
                context = {"message" : "Password Incorrect", "class": 'danger'}
                return render(request, 'accounts/login.html', context)

        elif end_user is not None and service_man is None: # is a end user
            user = authenticate(request, username = phone, password = password)
            if user is not None:
                login(request, user)
                request.session['phone'] = phone
                request.session['type'] = 1
                return redirect('home')
            else:
                context = {"message" : "Password Incorrect", "class": 'danger'}
                return render(request, 'accounts/login.html', context)

        else: # none
            context = {'message': 'User not found, please Register first', 'class': 'danger'}
            return render(request, 'accounts/login.html', context)

    return render(request, 'accounts/login.html')

def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        phone = request.POST.get('phone')

        check_user = User.objects.filter(email = email).first()
        check_enduser = EndUser.objects.filter(phone = phone).first()

        if check_user or check_enduser:
            context = {'message': 'User already exists', 'class': 'danger'}
            return render(request, 'accounts/register.html', context)

        user = User.objects.create_user(username = phone, email = email, first_name = name, password = password)
        user.save()

        enduser = EndUser(user = user, phone = phone)
        enduser.save()

        request.session['phone'] = phone
        request.session['type'] = 1
        return redirect(login_attempt)

    return render(request, 'accounts/register.html')

def register_sevice(request):
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
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

        user = User.objects.create_user(username = phone, email = email, first_name = company_name, password = password)
        user.save()

        service_man = serviceman(user = user, phone = phone,is_plumber=is_plumber,is_electrician=is_electrician,is_mechanic=is_mechanic,other_services=other_services,company_name=company_name)
        service_man.save()

        request.session['phone'] = phone
        request.session['type'] = 2
        return redirect(login_attempt)

    return render(request, 'accounts/register_sm.html')




def user_request(request):
    current_user = request.user
    service_requests = Request.objects.filter(customer_id = current_user.id)
    # print(service_requests)
    # for i in service_requests:
    #     print(i.requestid,i.rating,i.feedback)
    context = {
        'requests' : service_requests
    }

    return render(request, 'shop/user_page.html', context)

def serviceman_request(request):
    current_user = request.user
    service_requests = Request.objects.filter(serviceman_id = current_user.id)
    context = {
        'requests' : service_requests
    }
    if request.method=='POST' and 'updatedoa' in request.POST:
        dateApp = request.POST.get('DoA')
        id = request.POST.get('id')
        Request.objects.filter(requestid = id).update(doa = dateApp)
        context.update({"message":"Next doa added successfully"})
    
    if request.method=='POST' and 'complete' in request.POST:
        #dateApp = request.POST.get('DoA')
        id = request.POST.get('reqid')
        otp=request.POST.get('otp')
        if otp=="" or id=="":
            context.update({"message":"You did not enter otp or id","class":"danger"})
            return render(request, 'shop/request_staff.html', context)
        request1=Request.objects.filter(requestid = id).first()
        print(id)
        if str(otp)==str(request1.otp):
            Request.objects.filter(requestid = id).update(completed = True)
            context.update({"message":"Request marked as completed","class":"success"})
        else:
            context.update({"message":"Worng OTP","class":"danger"})
    
    return render(request, 'shop/request_staff.html', context)

def serviceman_completed_request(request):
    current_user = request.user
    service_requests = Request.objects.filter(serviceman_id = current_user.id)
    context = {
        'requests' : service_requests
    }
    return render(request, 'shop/request_completed_list.html', context)

def serviceman_inprogress_request(request):
    current_user = request.user
    service_requests = Request.objects.filter(serviceman_id = current_user.id)
    context = {
        'requests' : service_requests
    }
    if request.method=='POST' and 'updatedoa' in request.POST:
        dateApp = request.POST.get('DoA')
        id = request.POST.get('id')
        Request.objects.filter(requestid = id).update(doa = dateApp)
        context.update({"message":"Next doa added successfully"})
    
    if request.method=='POST' and 'complete' in request.POST:
        #dateApp = request.POST.get('DoA')
        id = request.POST.get('reqid')
        otp=request.POST.get('otp')
        if otp=="" or id=="":
            context.update({"message":"You did not enter otp or id","class":"danger"})
            return render(request, 'shop/request_inprogress_list.html', context)
        request1=Request.objects.filter(requestid = id).first()
        print(id)
        if str(otp)==str(request1.otp):
            Request.objects.filter(requestid = id).update(completed = True)
            context.update({"message":"Request marked as completed","class":"success"})
        else:
            context.update({"message":"Worng OTP","class":"danger"})
    
    return render(request, 'shop/request_inprogress_list.html', context)



def feedback_page(request,requestid):
    context={}
    if request.method == 'POST':
        # request_id = request.POST['request']
        request.session['request_id'] = requestid
        comment = request.POST.get('feedback')
        rating = request.POST.get('rating')
        service_request = Request.objects.filter(requestid = requestid)
        print("service_request =>",service_request)
        print(comment)
        print(rating)
        service_request.update(feedback = comment,rating = rating)
        context = {
            'service_request' : service_request
        }

    return render(request, 'shop/feedback_page.html', context)

def thankyou_page(request):
    phone = request.session['phone']
    print(phone)
    # type_ = request.session['type']
    context = {'message':'Successful'}

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

## this function to search for a word in a list of words in O(nlogn) complexity ###
# input: L (a list of words), target (word to be searched)
# output: None( if value is not found), target(if found)
def binary_search(L, target):
    i = 0
    j = len(L) - 1
    while i <= j:
        middle = (i + j)//2
        midpoint = L[middle]
        if midpoint > target:
            j = middle - 1
        elif midpoint < target:
            i = middle + 1
        else:
            return midpoint

path = 'F:/Pythons/resources/iron1.jpg'
faucet_url1 = 'https://www.aquantindia.com/wp-content/uploads/2020/04/Faucets-in-Chrome-Finish.jpg'
# file = Image.open('F:/Pythons/resources/iron1.jpg')
# file.show()


"""
function to classify image into respective department
input: string depicting exact path of the file or public url of the image
output: string containing department i.e. "plumber" or "electrical" 
        corresponding error message in case of failure
"""
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

    plumber_set = ['faucet','pipes','pipe','shower','wash','basin','water','washcloset','bathroom','water closet','flush','bathtub','steel','plumber','plumbing','wet']
    electrical_set = ['electrical','electronics','power','appliance','computer','conditioner','technology','wire','connection','switch','electricity','lamp','ceiling','fan','heater']  
    score_plumber = 0
    score_electrical =0
    
    ##### has n^2 complexity
    # for tag in tags: 
    #     if(tag in plumber_set):
    #         score_plumber+=1
    #     if(tag in electrical_set):
    #         score_electrical+=1

    ##### has nlog(n) complexity
    for word in tags:
        if binary_search(plumber_set,word) is not None:
            score_plumber+=1
        if binary_search(electrical_set,word) is not None:
            score_electrical+=1

    print("score_plumber =",score_plumber)
    print("score_electrical =",score_electrical)
    
    if(max(score_electrical,score_plumber)==0):
        return "something went wrong, could not predict the department"
    else:
        if(score_plumber>=score_electrical):
            return "plumber"
        else:
            return "electrical"


def add_request(request):
    context={}
    if request.method == 'GET':
        all_request = Request.objects.all()
        context = {"requests": all_request}
        return render(request,"shop/add_request.html",context)
#     if request.method == 'POST' and 'checkimage' in request.POST:
# #         requestid = request.POST.get('requestid')
#         # accepted = request.POST.get('accepted')
#         # customer_id = request.POST.get('customer_id')
#         image = request.POST.get("img")
#         category=classification(image)
#         context.update({'category': category,'image':image})
        
        
    if request.method == 'POST' and 'checkfile' in request.POST:
        if len(request.FILES) == 0:
            context = {"message": "No image uploaded", "class": "danger"}
            return render(request, "shop/add_request.html", context)
        image_uploaded = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image_uploaded.name, image_uploaded)
        uploaded_file_url = fs.url(filename)
        image = os.path.join(MEDIA_ROOT,filename)
        print(image)
        category=classification(image)
        context.update({'category': category ,'image':image})

    
    if request.method == 'POST' and 'submit_request' in request.POST:
        current_user = request.user
        print(current_user.id)
        department=request.POST.get('department')
        address=request.POST.get('address')
        print(address)
        if address=="":
            context = {"message": "Please enter the address", "class": "danger",'category':department}
            return render(request, "shop/add_request.html", context)
        deptnew = request.POST.get('dept')
        print(deptnew)
        otp=random.randint(1000,9999)
        if(deptnew != "select department" and deptnew!=""): #overriding the prediction by ML model
            department = deptnew
        given_request = Request(customer_id=current_user.id,department=department,address=address,otp=otp)
        given_request.save()
        context = {"message": "Request added successfully", "class": "success","status":201}
    
    return render(request, "shop/add_request.html", context)
#                                 # accepted = accepted    ,
#                                 department = department,
#                                 # completed = completed,
#                                 # rating = rating,
#                                 # feedback = feedback
#                                 )
#         given_request.save()
#         typee = request.session.get('type')
#         image = request.POST.get("img")
#         dept_drop = request.POST.get("dropDownDept")
#         car = request.POST.get("carSelected")
#         print("type => ",typee)
#         print("image=>",image)
#         print("dept_drop =>", dept_drop)
#         print("car =>",car)
#         dept = "default_dept"
#         # dept = classification(image)
#         # print("department predicted =>",department)
# #         serviceman_id = request.POST.get('serviceman_id')
# #         cost = request.POST.get('cost')
# #         ispaid = request.POST.get('is_paid')
#         department = request.POST.get('department',"_")
#         # completed = request.POST.get('completed')
#         # rating = request.POST.get('rating')
#         # feedback = request.POST.get('feedback')
         # given_request = Request(
#                                 # accepted = accepted    ,
#                                 department = department,
#                                 # completed = completed,
#                                 # rating = rating,
#                                 # feedback = feedback
#                                 )
#         given_request.save()
#         context = {"message": "Successful", "class": "OK","status":201}
#         if 'checkimage' in request.POST:
#             image = request.POST.get("img")
#             category=classification(image)
#             context.update({'category': category})
        
#this view will be responsible for
# 1.) GET - Viewing all the appointments of a request with given request id, 
#           with corresponding fields of remarks and date of appointment
# 2.) POST- will be used for passing the remarks from the enduser and service staff 
#           for a particular visit/appointment

def appointments(request,reqid):
    # context = {}
    # print("*****************************\nreqid =",reqid)
    # req_object = Request.objects.filter(requestid=reqid)[0]
    # all_appointments = Appointments.objects.filter(requestid=req_object)


    req_object = Request.objects.filter(requestid=reqid)[0]
    isCompleted = req_object.completed
    all_appointments = Appointments.objects.filter(requestid=req_object)
    context = {'reqid':reqid,"isCompleted":isCompleted,"appointments":all_appointments}
    if request.method=="GET":
        # date = request.GET.get('DoA')
        # id = request.GET.get('id')
        # id_appointments = Appointments.objects.filter(requestid=id)
        print("inside GET ReQUEST for appointments")
        
        # print("\n\nHERE ****************************> \n",req_object.serviceman_id,req_object.customer_id)
        all_appointments = Appointments.objects.filter(requestid=req_object)
        # print(len(all_appointments))
        context.update({"appointments":all_appointments})
        return render(request,"shop/appointments.html",context)
    
    if request.method=="POST":
        # date = request.GET.get('DoA')
        # id = request.GET.get('id')
        # purpose = request.GET.get('purpose')
        # remarksfromuser = request.GET.get('remarksFromUser')
        # remarskfromstaff = request.GET.get('remarksFromStaff')

        if('createNewAppointment' in request.POST):
            print("-------------------creating new appointment--------------------")
            purpose = request.POST.get('purpose',"")
            dateofapp = request.POST.get('DoA')
            print(dateofapp)
            print(purpose)
            newapp = Appointments(requestid = req_object,doa=dateofapp,purpose=purpose)
            newapp.save()
        else:
            date = request.POST.get('DoA')
            date = parse(date).date()
            # print(date, type(date))
            app_object = Appointments.objects.filter(requestid=req_object, doa=date)
            # print("see here , ", app_object, len(app_object), app_object[0].doa)
            # id = request.POST.get('id')
            # purpose = request.POST.get('purpose')
            remarksfromuser = request.POST.get('remarksFromUser')
            remarksfromstaff = request.POST.get('remarksFromStaff')
            print("remarks here \n\n\n\n\n", remarksfromstaff, remarksfromuser)
            if remarksfromuser != None:
                # req_object.remark_from_user = remarksfromuser
                app_object.update(remark_from_user = remarksfromuser)
            if remarksfromstaff != None:
                # req_object.remark_from_staff = remarksfromstaff
                app_object.update(remark_from_staff = remarksfromstaff)
            print("\n\nnew remarks saved\n\n")
        #### to be discussed and completed
        
        all_appointments = Appointments.objects.filter(requestid=req_object)
        context.update({"appointments":all_appointments})
        
        #### trigger to update next date of appointment field in Request table
        for app in all_appointments:
            print("appointment date =",app.doa, "today = ",datetime.date.today())
            if(app.doa >= datetime.date.today()):
                nextdoa = app.doa
                break
        context.update({"nextdoa":nextdoa})
        Request.objects.filter(requestid=reqid).update(doa=nextdoa)
        ##### endtrigger
        return render(request,"shop/appointments.html",context)


def staff_request(request):    
    all_request = Request.objects.all()
    context = {"requests": all_request}
    if request.method == 'GET':        
        return render(request,"shop/staff_page.html",context)
    if request.method == 'POST':
        requestid = request.POST.get('id')
        print("===========================\n",request.POST)
        current_user = request.user
        dateofapp = request.POST.get('DoA')
        if dateofapp=="":
            context.update({"message": "You did not enter date of appointment", "class": "danger"})
            return render(request, "shop/staff_page.html", context)
        purpose = request.POST.get('purpose',"Initial Inspection")
        # print("=====================\ndate=",dateofapp,"\nrequestid=",requestid)
        # Request.objects.filter(requestid=requestid).update(accepted=1,serviceman_id=current_user.id,doa = dateofapp)
        # newappointment = Appointments(requestid=requestid,doa=dateofapp,purpose=purpose)
        # newappointment.save()
        print("=====================\ndate=",dateofapp,"\nrequestid=",requestid)
        Request.objects.filter(requestid=requestid).update(accepted=1,serviceman_id=current_user.id,doa = dateofapp)
        req_object = Request.objects.filter(requestid=requestid)[0]
        
        newappointment = Appointments(requestid=req_object,doa=dateofapp,purpose=purpose)
        newappointment.save()
        # print("Its here")
#         requestid = request.POST.get('requestid')
#         accepted = request.POST.get('accepted')
# #        customer_id = request.POST.get('customer_id')
# #         serviceman_id = request.POST.get('serviceman_id')
#         cost = request.POST.get('cost')
# #         ispaid = request.POST.get('is_paid')
#         department = request.POST.get('department')
#         completed = request.POST.get('completed')
# #         rating = request.POST.get('rating')
# #         feedback = request.POST.get('feedback')
#         given_request = Request( 
#                                 accepted = accepted    ,
#                                 cost = cost,
#                                 department = department,
#                                 completed = completed,
                               
#                                 )
#         given_request.save()
        context.update({"message": "Successful", "class": "OK","status":201})
        # context = {"message": "No request found", "class": "danger","status":404}
        return render(request, "shop/staff_page.html", context)

def home(request):
    current_user = request.user
    if current_user.is_staff:
        return redirect('staff_page')
    return redirect('user_page')
