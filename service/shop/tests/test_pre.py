from django.test import TestCase
from shop.models import *
from django.utils import timezone
# from django.core.urlresolvers import reverse
# from whatever.forms import WhateverForm
# Create your tests here.

#Model Test
# class EndUserTest(TestCase):
#     user = User.objects.create_user(username = "tester671", email = "email", first_name = "name", password = "password")
#     phone='+999999999'
#     def create_enduser(self):
#         return EndUser.objects.create(user = self.user, phone = self.phone)


#     def test_enduser_creation(self):
#         T = self.create_enduser()
#         self.assertTrue(isinstance(T, EndUser))
#         self.assertEqual(phone,T.phone)

    
# class RequestTest(TestCase):
#     def create_request(self):
#         return Request.objects.create()

#     def test_request_creation(self):
#         T = self.create_request()
#         self.assertTrue(isinstance(T,Request))
#         self.assertEqual(T.__str__(),T.requestid)


# # Views Test
# class AddRequestTest(TestCase):
#     @classmethod
#     def setupdata(cls):
#         num_request = 17
#         for _ in range(num_request):
#             Request.objects.create()

#     def test_get_status_response(self):
#         response = self.client.get('add_request')
#         self.assertTemplateUsed(response, 'shop/add_request.html')
#         # self.assertEqual(response.status_code, 200)