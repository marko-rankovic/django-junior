from . import  views
from django.conf.urls import  url

app_name = 'signup'

urlpatterns = [
    url(r'^$', views.RegistrationView.as_view(), name= 'index')
]