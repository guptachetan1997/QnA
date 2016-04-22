from django import template
from notifications.models import Notification

register = template.Library()

@register.simple_tag
def count(id):
    count = Notification.objects.filter(user_id=id, status_read=False).count()
    return str(count)

@register.assignment_tag
def get_notifs_user(user_id):
    notifs = Notification.objects.filter(user_id = user_id, status_read=False).order_by("-timestamp")
    return notifs[:5]
