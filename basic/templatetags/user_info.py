from django import template
from django.contrib.auth.models import User
from userprofile.models import UserProfile

register = template.Library()

@register.simple_tag
def get_username_from_userid(user_id):
    try:
        return User.objects.get(id=user_id).username
    except User.DoesNotExist:
        return 'Unknown'

@register.simple_tag
def get_fullname_from_userid(user_id):
    try:
        u = User.objects.get(id=user_id)
        return u.first_name + " " + u.last_name
    except User.DoesNotExist:
        return 'Unknown'

@register.simple_tag
def get_profile_pic_from_userid(user_id):
    try:
        return UserProfile.objects.get(user_id=user_id).profile_pic.url
    except User.DoesNotExist:
        return 'Unknown'
