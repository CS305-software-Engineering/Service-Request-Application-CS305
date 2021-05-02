from django.contrib import admin
from django.urls import reverse,resolve
from django.test import SimpleTestCase
from shop.views import home,login,login_attempt,register,user_request,appointments,staff_request,feedback_page,serviceman_completed_request,serviceman_inprogress_request,serviceman_request

class TestUrls(SimpleTestCase):
    
    def test_home(self):
        url = reverse('home')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,home)

    def test_register(self):
        url = reverse('register')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,register)

    def test_staff_page(self):
        url = reverse('staff_page')
        # print(resolve(url))
        self.assertEquals(resolve(url).func,staff_request)

    def test_feedback_page(self):
        try:
            url = reverse('feedback_page',args=["d"])
            assert 1==2
        except:
            pass
        url = reverse('feedback_page',args=[2])
        # print(resolve(url))
        self.assertEquals(resolve(url).func,feedback_page)
        url = reverse('feedback_page',args=["3"])
        # print(resolve(url))
        self.assertEquals(resolve(url).func,feedback_page)
    
    def test_appointments_page(self):
        try:
            url = reverse('appointments',args=["d"])
            assert 1==2
        except:
            pass
        url = reverse('appointments',args=[2])
        # print(resolve(url))
        self.assertEquals(resolve(url).func,appointments)
        url = reverse('appointments',args=["3"])
        # print(resolve(url))
        self.assertEquals(resolve(url).func,appointments)