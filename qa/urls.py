from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^(?P<id>\d+)$', views.single),
    url(r'^s/(?P<ans_id>\d+)$', views.single_ans),
    url(r'^$', views.all),
    url(r'^add_ques', views.add_ques),
    url(r'^search', views.search, name='search'),
    url(r'^questions', views.only_questions),
    url(r'^add_ans/(?P<q_id>\d+)', views.add_ans),
    url(r'^upvote_ques/(?P<q_id>\d+)', views.up_ques),
    url(r'^downvote_ques/(?P<q_id>\d+)', views.down_ques),
    url(r'^upvote_ans/(?P<ans_id>\d+)', views.up_ans),
    url(r'^downvote_ans/(?P<ans_id>\d+)', views.down_ans),
]
