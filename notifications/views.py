from django.shortcuts import render,redirect
from models import Notification
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/accounts/login/')
def display_noti(request):
    iD = request.user.id
    flag = False
    if Notification.objects.filter(user_id=iD, status_read=False).exists():
        notifications = Notification.objects.filter(user_id=iD, status_read=False).order_by("-timestamp")
        flag=True
    else:
        notifications = {'None to show'}
    return render(request, 'notifications/display_noti.html',{'notifications':notifications, 'flag':flag})

@login_required(login_url='/accounts/login/')
def notif_read(request, id):
    if id:
        a = Notification.objects.get(id = id)
        a.status_read = True
        a.save()
        return HttpResponseRedirect('/notifications/display/')

@login_required(login_url='/accounts/login/')
def notif_read_all(request):
    iD = request.user.id
    if Notification.objects.filter(user_id=iD, status_read=False).exists():
        notifs = Notification.objects.filter(user_id=iD, status_read=False)
        for notif in notifs:
            notif.status_read = True
            notif.save()
        return HttpResponseRedirect('/notifications/display/')
