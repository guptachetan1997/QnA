from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^(?P<user_id>\d+)$', views.user_profile_display),
    url(r'^edit', views.user_profile_edit),
    url(r'^like/(?P<user_id>\d+)$', views.like_user),
]
