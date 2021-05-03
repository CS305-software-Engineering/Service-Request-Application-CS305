# from django.contrib import admin
from django.urls import reverse,resolve
from django.test import TestCase, Client
from shop.models import EndUser, Request, Appointments, serviceman
import time

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        Request.objects.create(
            requestid=1,
            customer_id="c1",
            serviceman_id="s1",
            department="electrical"
        )
        self.serviceman_completed_request_url = reverse('serviceman_completed_request')
        self.appointments_url = reverse('appointments',args=[1])
        self.register_url = reverse('register')
        self.add_request_url = reverse('add_request')
        self.login_url = reverse('login_attempt')
        self.feedback_url = reverse("feedback_page",args=[1])
    
    def test_register_GET(self):
        print("Testing_views................ register - GET",end="")
        response = self.client.get(self.register_url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'accounts/register_new.html')

    def test_register_POST(self):
        print("Testing_views................ register new user - POST",end="")
        response = self.client.post(self.register_url,{
            "email" : "email@123.com",
            "password" : "password",
            "name" : "name",
            "phone" : "9876543210",
        })
        self.assertEquals(response.status_code,302)
        self.assertEquals(len(EndUser.objects.filter(phone="9876543210")),1)

        response = self.client.post(self.register_url,{ #duplicate phone number 
            "email" : "john@gmail.com",
            "password" : "password",
            "name" : "john",
            "phone" : "9876543210",
        })
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.context.get('class'),'danger')
        response = self.client.post(self.register_url,{ #unique phone number but same email address
            "email" : "email@123.com",
            "password" : "password",
            "name" : "johnathan",
            "phone" : "9876543212",
        })
        
        self.assertEquals(len(EndUser.objects.filter(phone="9876543210")),1)
        self.assertEquals(response.status_code,200)
        self.assertEquals(response.context.get('class'),'danger')
        # print(len(EndUser.objects.filter(phone="9876543210")),len(EndUser.objects.filter(phone="9876543212")),len(EndUser.objects.all()))
        
    def test_login_GET(self):
        print("Testing_views................ register - GET",end="")
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'accounts/login_new.html')
    
    def test_login_POST(self):
        print("Testing_views................ login - POST",end="")
        response = self.client.post(self.login_url,{
            "phone":"9876543210",
            "password":"password"
        })


    # def test_add_request_post(self):
    #     print("Testing_views................ add_request - POST",end="")
    #     response = self.client.post(self.add_request_url,
    #         {
    #             'requestid':2,
    #             "customer_id":"c2",
    #             "serviceman_id":"s2",
    #             "department":"plumber",
    #             "submit_request":"2"
    #         }
    #     )
    #     queryset = Request.objects.filter(requestid=2)
    #     print("entries with requestid 2 =>",len(queryset))
    #     queryset = Request.objects.all()
    #     print("total entries =>",len(queryset))

    #     self.assertEquals(response.status_code,200)

    # def test_serviceman_completed_requests_GET(self):
    #     print("Testing_views................ serviceman_completed_requests",end="")
    #     response = self.client.get(self.serviceman_completed_request_url)

    #     self.assertEquals(response.status_code,200)
    #     self.assertTemplateUsed(response, 'shop/request_completed_list.html')

    def test_feedback_GET(self):
        print("Testing_views................ feedback_api GET",end="")
        response = self.client.get(self.feedback_url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, 'shop/feedback_page.html')


    # def test_serviceman_completed_requests_GET(self):
    #     print("Testing_views................ serviceman_completed_requests",end="")
    #     response = self.client.get(self.serviceman_completed_request_url)

    #     self.assertEquals(response.status_code,200)
    #     self.assertTemplateUsed(response, 'shop/request_completed_list.html')