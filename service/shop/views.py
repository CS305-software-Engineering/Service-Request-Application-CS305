from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import CreateView

# Create your views here.
from shop.forms import EndUserSignUpForm
from shop.models import User

class EndUserSignUpView(CreateView):
    model = User
    form_class = EndUserSignUpForm
    template_name = "registration/signup_form.html"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'enduser'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/admin')
