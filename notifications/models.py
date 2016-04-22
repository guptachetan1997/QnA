from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status_read = models.BooleanField(default = False)
    user = models.ForeignKey(User)
    link = models.CharField(blank=True, max_length=50)

    def __str__(self):
        return self.title

def add_notif_user(notif, user_id):
    notif = Notification(
            title = notif['title'],
            body = notif['body'],
            user_id = user_id,
            link = notif['link']
    )
    notif.save()

def notif_all_except(noti, user_id):
    users = User.objects.exclude(id = user_id)
    for user in users:
        notif = Notification(
                title = noti['title'],
                body = noti['body'],
                user_id = user.id,
                link = noti['link']
        )
        notif.save()
