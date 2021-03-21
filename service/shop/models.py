from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class User(AbstractUser):
    is_enduser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

class EndUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=False)
    
class serviceman(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    company_name = models.CharField(max_length=100,default="Freelancer")
    is_plumber = models.BooleanField(default=False)
    is_electrician = models.BooleanField(default=False)
    is_mechanic = models.BooleanField(default=False)
    other_services = models.CharField(max_length=100,default="None")
