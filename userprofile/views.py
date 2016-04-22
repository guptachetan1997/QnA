from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from models import UserProfile
from qa.models import Question,Answer
from blog.models import Post
from django.contrib.auth.models import User

@login_required(login_url='/accounts/login/')
def user_profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES or None, instance=request.user.profile)
        if form.is_valid():
            user_profile_form = form.save(commit = False)
            user_profile_form.user = User.objects.get(id = request.user.id)
            user_profile_form.save()
            return HttpResponseRedirect('/profile/%s' %request.user.id)
        else:
            return HttpResponseRedirect('/profile/%s' %request.user.id)
    else:
        user = request.user
        profile = user.profile
        form = UserProfileForm(instance=profile)
        args = {}
        args.update(csrf(request))
        args['form'] = form
        return render(request, 'userprofile/profile.html', args)

@login_required(login_url='/accounts/login/')
def user_profile_display(request, user_id):
    profile_basics = User.objects.get(id = user_id)
    profile_contents = UserProfile.objects.get(user_id= user_id)
    user_info = {}
    user_info['questions'] = Question.objects.filter(user_id = user_id, anonymous=False).order_by("-date")
    user_info['question_count'] = Question.objects.filter(user_id = user_id, anonymous=False).count()
    user_info['answers'] = Answer.objects.filter(user_id = user_id, anonymous=False).order_by("-timestamp")
    user_info['answer_count'] = Answer.objects.filter(user_id = user_id, anonymous=False).count()
    user_info['blogs'] = Post.objects.filter(user_id = user_id).order_by("-date")
    user_info['blog_count'] = Post.objects.filter(user_id = user_id).order_by("-date").count()

    return render(request, 'userprofile/profile_display.html' , {'profile_contents': profile_contents, 'profile_basics':profile_basics, 'user_info':user_info})

@login_required(login_url='/accounts/login/')
def like_user(request, user_id):
    u = UserProfile.objects.get(user_id = user_id)
    u.likes+=1
    u.save()
    return HttpResponseRedirect('/profile/%s' % user_id)
