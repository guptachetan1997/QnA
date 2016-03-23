from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    q_text = models.CharField(max_length=200)
    q_body = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    anonymous = models.BooleanField(default=False)
    ans_count = models.IntegerField(default=0)

    def __str__(self):
        return self.q_text

class Answer(models.Model):
    ans_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    anonymous = models.BooleanField(default=False)
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.ans_text[:100]

class Comment(models.Model):
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    answer = models.ForeignKey(Answer)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.body[:100]
