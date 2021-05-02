from .views import *
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/login')),
    path('login', login_attempt, name='login_attempt'),
    path('register', register, name='register'),
    path('register_service-man',register_sevice,name='register_service'),
    path('home',home, name='home'),
    path('staff_page', staff_request, name='staff_page'),
    path('user_page', user_request, name='user_page'),
    path('add_request', add_request, name='add_request'),
    path('feedback_page/<int:requestid>', feedback_page, name='feedback_page'),
    path('thankyou', thankyou_page, name='thankyou_page'),
    path('serviceman_request',serviceman_request,name='serviceman_request'),
    path('serviceman_completed_request',serviceman_completed_request,name='serviceman_completed_request'),
    path('serviceman_inprogress_request',serviceman_inprogress_request,name='serviceman_inprogress_request'),
    path('appointments/<str:reqid>',appointments,name="appointments")
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
