from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from phonenumber_field.form_fields import PhoneNumberField

from shop.models import EndUser, User

class EndUserSignUpForm(UserCreationForm):
    phone = PhoneNumberField()

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_enduser = True
        user.save()

        enduser = EndUser.objects.create(user=user)
        enduser.phone.add(*self.cleaned_data.get('phone'))

        return user