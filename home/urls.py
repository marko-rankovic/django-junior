from . import  views
from django.conf.urls import  url


app_name = 'home'

urlpatterns = [
    url(r'^$', views.UsersView.as_view(), name= 'index'),
    url(r'^(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name= 'profile'),
]
