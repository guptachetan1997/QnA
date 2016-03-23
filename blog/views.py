from django.shortcuts import render, redirect
from blog.models import Post,Blog_Comment
from django.contrib.auth.decorators import login_required
from forms import PostForm,AddComment
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from notifications.models import *
from django.contrib.auth.models import User


@login_required(login_url='/accounts/login/')
def all(request):
    return render(request, 'blog/blog.html', {"posts": Post.objects.all().order_by("-date"),})

@login_required(login_url='/accounts/login/')
def single(request,id):
    if id:
        if request.POST:
            form = AddComment(request.POST)
            if form.is_valid():
                comment_form = form.save(commit = False)
                comment_form.user = request.user
                comment_form.post = Post.objects.get(id=id)
                comment_form.save()
                return HttpResponseRedirect('/blog/%s' % id)
            else:
                return HttpResponseRedirect('/blog/%s' % id)
        else:
            args = {}
            args.update(csrf(request))
            args['form'] = AddComment()
            p = Post.objects.get(id=id)
            p.view +=1
            p.save()
            args['post'] = Post.objects.get(id=id)
            args['comments'] = Blog_Comment.objects.filter(post_id = id)
            args['comment_count'] = Blog_Comment.objects.filter(post_id = id).count()
            return render(request, 'blog/post.html', args)

@login_required(login_url='/accounts/login/')
def create(request):
    if request.POST:
        form = PostForm(request.POST)
        if form.is_valid():
            post_form = form.save(commit = False)
            post_form.user = request.user
            post_form.save()
            notif_all_except(
                {
                    'title': request.user.username + " added a new blogpost.",
                    'body' : post_form.title,
                    'link' : "/blog/%s"%post_form.id
                },
                request.user.id
            )
            return redirect('/blog/')
        else:
            return redirect('/blog/')
    else:
        args = {}
        args.update(csrf(request))
        args['form'] = PostForm()
        return render(request, 'blog/create_post.html', args)
