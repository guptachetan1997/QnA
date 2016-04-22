from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^qa/', include('qa.urls', namespace='qa')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^profile/', include('userprofile.urls')),
    url(r'^accounts/login', views.log_in, name="login"),
    url(r'^accounts/auth_view', views.auth_view),
    url(r'^accounts/logout', views.log_out, name="logout"),
    url(r'^accounts/register', views.register, name="register"),
    url(r'^notifications/', include('notifications.urls')),
    # url(r'^accounts/register_fail', views.register_fail, name="register_fail"),
]
