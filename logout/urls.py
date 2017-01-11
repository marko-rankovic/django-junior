from . import  views
from django.conf.urls import  url

app_name = 'login'

urlpatterns = [
    url(r'^$', views.LogoutView.as_view(), name='index')
]