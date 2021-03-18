from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(AbstractUser):
    is_enduser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

class EndUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    