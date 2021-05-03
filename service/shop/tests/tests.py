from django.test import TestCase
from shop.models import *
from django.utils import timezone
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
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


# Views Test
# class AddRequestTest(TestCase):
#     @classmethod
#     def setupdata(cls):
#         num_request = 17
#         for _ in range(num_request):
#             Request.objects.create()

#     def test_get_status_response(self):
#         response = self.client.get('add_request')
#         self.assertTemplateUsed(response, 'shop/add_request.html')
        # self.assertEqual(response.status_code, 200)

# class LoginTest(LiveServerTestCase):

#   def test(self):
#     # selenium = webdriver.Chrome()
#     selenium = webdriver.Firefox()
#     #Choose your url to visit
#     selenium.get('http://127.0.0.1:8000/login')
#     #find the elements you need to submit form
#     phone = selenium.find_element_by_name('phone')
#     password = selenium.find_element_by_name('password')
#     # player_name = selenium.find_element_by_id('id_name')
#     # player_height = selenium.find_element_by_id('id_height')
#     # player_team = selenium.find_element_by_id('id_team')
#     # player_ppg = selenium.find_element_by_id('id_ppg')

#     submit = selenium.find_element_by_name('loginsubmit')

#     #populate the form with data
#     phone.send_keys('7777777777')
#     password.send_keys('Service@123')
#     # player_name.send_keys('Lebron James')
#     # player_team.send_keys('Los Angeles Lakers')
#     # player_height.send_keys('6 feet 9 inches')
#     # player_ppg.send_keys('25.7')
#     print("before",selenium.current_url)
#     #submit form
#     submit.send_keys(Keys.RETURN)
#     time.sleep(2)
#     print("after",selenium.current_url)
#     #check result; page source looks at entire html document
#     assert '7777777777' in selenium.page_source
#     selenium.close()