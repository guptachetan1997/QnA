from django.shortcuts import render
from models import Question,Answer,Comment,Vote
from blog.models import Post
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from forms import QuestionForm,AnswerForm,AddComment
from notifications.models import add_notif_user,notif_all_except
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.db.models import Q

@login_required(login_url='/accounts/login/')
def search(request):
    query  = request.GET.get('search', '')
    questions = Question.objects.filter( Q(q_text__icontains=query) | Q(tags__icontains=query) ).order_by("-date")
    posts = Post.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)).order_by("-date")
    profiles = User.objects.filter(Q(username__icontains=query)| Q(first_name__icontains=query) | Q(last_name__icontains=query))
    return render(request, 'qa/search_r.html', {'questions':questions, 'posts':posts, 'profiles':profiles})


@login_required(login_url='/accounts/login/')
def all(request):
    questions = Question.objects.filter(ans_count__gt=0).order_by("-date")
    ans = Answer.objects.all()
    answers = []
    for question in questions:
        if ans.filter(question_id= question.id):
            answers.append(ans.filter(question_id = question.id).latest('timestamp'))
    return render(request, 'qa/all.html', {'data': zip(questions,answers)})

@login_required(login_url='/accounts/login/')
def only_questions(request):
    questions = Question.objects.all().order_by("ans_count","-date")
    return render(request, 'qa/questions.html', {'questions': questions})

@login_required(login_url='/accounts/login/')
def single_ans(request, ans_id):
    if ans_id:
        if request.POST:
            form = AddComment(request.POST)
            if form.is_valid():
                comment_form = form.save(commit = False)
                comment_form.answer = Answer.objects.get(id = ans_id)
                comment_form.user = User.objects.get(id = request.user.id)
                if comment_form.answer.user_id != request.user.id:
                    add_notif_user(
                        {
                            'title': comment_form.user.username + " commented on your answer.",
                            'body' : "",
                            'link' : "/qa/s/%s"%ans_id
                        },
                        comment_form.answer.user_id
                    )
                comment_form.save()
                return HttpResponseRedirect('/qa/s/%s' % ans_id)
            else:
                return HttpResponseRedirect('/qa/s/%s' % ans_id)
        else:
            args = {}
            args.update(csrf(request))
            answer = Answer.objects.get(id = ans_id)
            args['form'] = AddComment()
            args['question'] = Question.objects.get(id = answer.question_id)
            args['comments'] = Comment.objects.filter(answer_id = ans_id)
            args['comment_count'] = Comment.objects.filter(answer_id = ans_id).count()
            args['answer'] = Answer.objects.get(id = ans_id)
            return render(request, 'qa/single_ans.html', args)

@login_required(login_url='/accounts/login/')
def single(request, id):
    question = Question.objects.get(id = id)
    answers = Answer.objects.filter(question_id=id).order_by("-upvotes")
    data = answers
    return render(request, 'qa/single.html', {'question':question, 'data':data})


@login_required(login_url='/accounts/login/')
def add_ques(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_form = form.save(commit = False)
            question_form.user = User.objects.get(id = request.user.id)
            question_form.save()
            notif_all_except(
                {
                    'title': "A new question has been added",
                    'body' : question_form.q_text,
                    'link' : "/qa/%s"%question_form.id
                },
                request.user.id
            )
        return HttpResponseRedirect('/qa/')
    else:
        args = {}
        args.update(csrf(request))
        args['form'] = QuestionForm()
        return render(request, 'qa/add_ques.html', args)

@login_required(login_url='/accounts/login/')
def add_ans(request, q_id):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer_form = form.save(commit = False)
            answer_form.user = User.objects.get(id = request.user.id)
            q = Question.objects.get(id = q_id)
            q.ans_count+=1
            q.save()
            answer_form.question = q
            answer_form.save()
            if answer_form.anonymous is True:
                username = "Anonymous"
            else:
                username = answer_form.user.username
            add_notif_user(
                {
                    'title': username + " added a answer to your question.",
                    'body' : "",
                    'link' : "/qa/s/%s"%answer_form.id
                },
                answer_form.question.user_id
            )
        return HttpResponseRedirect('/qa/%s' % q_id)
    else:
        args = {}
        args.update(csrf(request))
        args['form'] = AnswerForm()
        args['q_id'] = q_id
        return render(request, 'qa/add_ans.html', args)

@login_required(login_url='/accounts/login/')
def up_ques(request, q_id):
    content_type = ContentType.objects.get_for_model(Question)
    try:
        vote = Vote.objects.get(content_type=content_type, object_id=q_id, user_id=request.user.id)
        if vote.value == 1:
            q = Question.objects.get(id = q_id)
            q.upvotes-=1
            q.save()
            vote.delete()
        else:
            q = Question.objects.get(id = q_id)
            q.downvotes+=1
            q.save()
            vote.delete()
            return HttpResponseRedirect('/qa/upvote_ques/%s' % q_id)

    except Vote.DoesNotExist:
        q = Question.objects.get(id = q_id)
        q.upvotes+=1
        q.save()
        v = Vote()
        v.user_id = request.user.id
        v.value = 1
        v.content_object = q
        v.save()
        add_notif_user(
            {
                'title': request.user.username + " upvoted your question.",
                'body' : "",
                'link' : "/qa/%s"%q_id
            },
            q.user_id
        )
    return HttpResponseRedirect('/qa/%s' % q_id)

@login_required(login_url='/accounts/login/')
def down_ques(request, q_id):
    content_type = ContentType.objects.get_for_model(Question)
    try:
        vote = Vote.objects.get(content_type=content_type, object_id=q_id, user_id=request.user.id)
        if vote.value == -1:
            q = Question.objects.get(id = q_id)
            q.downvotes+=1
            q.save()
            vote.delete()
        else:
            q = Question.objects.get(id = q_id)
            q.upvotes-=1
            q.save()
            vote.delete()
            return HttpResponseRedirect('/qa/downvote_ques/%s' % q_id)

    except Vote.DoesNotExist:
        q = Question.objects.get(id = q_id)
        q.downvotes-=1
        q.save()
        v = Vote()
        v.user_id = request.user.id
        v.value = -1
        v.content_object = q
        v.save()
        add_notif_user(
            {
                'title': request.user.username + " downvoted your question.",
                'body' : "",
                'link' : "/qa/%s"%q_id
            },
            q.user_id
        )
    return HttpResponseRedirect('/qa/%s' % q_id)

@login_required(login_url='/accounts/login/')
def up_ans(request, ans_id):
    content_type = ContentType.objects.get_for_model(Answer)
    try:
      vote = Vote.objects.get(content_type=content_type, object_id=ans_id, user_id=request.user.id)
      if vote.value == 1:
          a = Answer.objects.get(id = ans_id)
          a.upvotes-=1
          a.save()
          vote.delete()
      else:
          a = Answer.objects.get(id = ans_id)
          a.downvotes+=1
          a.save()
          vote.delete()
          return HttpResponseRedirect('/qa/upvote_ans/%s' % ans_id)
    except Vote.DoesNotExist:
        a = Answer.objects.get(id = ans_id)
        a.upvotes+=1
        a.save()
        v = Vote()
        v.user_id = request.user.id
        v.value = 1
        v.content_object = a
        v.save()
        add_notif_user(
        {
            'title': request.user.username + " upvoted your answer.",
            'body' : "",
            'link' : "/qa/s/%s"%ans_id
        },
        a.user_id
    )
    return HttpResponseRedirect('/qa/s/%s' % ans_id)


@login_required(login_url='/accounts/login/')
def down_ans(request, ans_id):
    content_type = ContentType.objects.get_for_model(Answer)
    try:
      vote = Vote.objects.get(content_type=content_type, object_id=ans_id, user_id=request.user.id)
      if vote.value == -1:
          a = Answer.objects.get(id = ans_id)
          a.downvotes+=1
          a.save()
          vote.delete()
      else:
          a = Answer.objects.get(id = ans_id)
          a.upvotes-=1
          a.save()
          vote.delete()
          return HttpResponseRedirect('/qa/downvote_ans/%s' % ans_id)
    except Vote.DoesNotExist:
        a = Answer.objects.get(id = ans_id)
        a.downvotes-=1
        a.save()
        v = Vote()
        v.user_id = request.user.id
        v.value = -1
        v.content_object = a
        v.save()
        add_notif_user(
        {
            'title': request.user.username + " downvoted your answer.",
            'body' : "",
            'link' : "/qa/s/%s"%ans_id
        },
        a.user_id
    )
    return HttpResponseRedirect('/qa/s/%s' % ans_id)
