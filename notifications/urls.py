from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^display', views.display_noti),
    url(r'^notif_read/(?P<id>\d+)$', views.notif_read),
    url(r'^notif_read/all', views.notif_read_all),
]
