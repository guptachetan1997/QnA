from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm
from userprofile.models import UserProfile

def log_in(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/qa/')
    args = {}
    args.update(csrf(request))
    return render(request, 'basic/login.html', args)

def auth_view(request):
    username = request.POST.get('inputUsername', "")
    password = request.POST.get('inputPassword', "")
    user  = authenticate(username=username, password=password)
    # print request.POST.get('next') == ""
    if user is not None:
        login(request,user)
        if UserProfile.objects.filter(user_id= request.user.id).exists():
            if request.POST.get('next') == "":
                return HttpResponseRedirect('/qa/')
            else :
                return HttpResponseRedirect(request.POST.get('next'))
        else:
                return HttpResponseRedirect('/profile/edit')
    else:
        return HttpResponseRedirect('/accounts/login')

@login_required(login_url='/accounts/login/')
def log_out(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login')

def register(request):
    if request.user.is_authenticated():
        return redirect('/qa/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        flag = True
        if User.objects.filter(username=request.POST.get('username')).exists() or User.objects.filter(email=request.POST.get('email')).exists():
            flag = False
        if form.is_valid() and flag:
            form.save()
            return HttpResponseRedirect('/qa/')
        else:
            return HttpResponseRedirect('/accounts/register')
    else:
        args = {}
        args.update(csrf(request))
        args['form'] = RegistrationForm()
        return render(request, 'basic/register.html', args)
