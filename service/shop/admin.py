from django.contrib import admin
from .models import EndUser,serviceman, Request

# Register your models here.
admin.site.register(EndUser)
admin.site.register(serviceman)
admin.site.register(Request)