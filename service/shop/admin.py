from django.contrib import admin
from shop.models import EndUser

# Register your models here.
class EndUserAdmin(admin.ModelAdmin):
    list_display = ("username", "phone")

admin.site.register(EndUser, EndUserAdmin)