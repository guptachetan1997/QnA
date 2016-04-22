from django.conf.urls import url,include
from django.views.generic import ListView, DetailView
from . import views

urlpatterns = [
    url(r'^(?P<id>\d+)$', views.single),
    url(r'^$', views.all),
    url(r'^create/$', views.create),
]
