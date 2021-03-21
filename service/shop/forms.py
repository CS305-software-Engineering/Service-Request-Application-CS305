from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django import forms

from shop.models import EndUser, User

class EndUserSignUpForm(UserCreationForm):
    phone = forms.CharField(max_length=17, empty_value=False)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_enduser = True
        user.save()

        enduser = EndUser.objects.create(user=user)
        phone = self.cleaned_data.get('phone')
        enduser.phone = phone
        enduser.save()

        return user