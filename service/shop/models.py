from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator


#   python -m venv djangoenv
#   source djangoenv/bin/activate

# Model for End User
class EndUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=False)
    otp = models.CharField(max_length=6)
    
class serviceman(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=False)
    company_name = models.CharField(max_length=100,default="Freelancer")
    is_plumber = models.BooleanField(default=False)
    is_electrician = models.BooleanField(default=False)
    is_mechanic = models.BooleanField(default=False)
    other_services = models.CharField(max_length=100,default="None")
    otp = models.CharField(max_length=6,default="1111")

class Request(models.Model):
    requestid = models.AutoField(primary_key=True)
    accepted = models.IntegerField(default=-1)
    customer_id = models.CharField(default="_",max_length=200)
    serviceman_id = models.CharField(default="_",max_length=200)
    cost = models.FloatField(default=0.0,editable=True)
    ispaid = models.BooleanField(default=False,editable=True)
    department = models.CharField(default='_',max_length=200)
    completed = models.BooleanField(default=False,editable=True)
    rating = models.FloatField(default=-1)
    feedback = models.CharField(default='_',max_length=500)

