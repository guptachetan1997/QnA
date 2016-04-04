from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from markdown_deux import markdown
from django.utils.safestring import mark_safe

class Post(models.Model):
    title = models.CharField(max_length = 140)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    view = models.IntegerField(default=0)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.title

    def get_markdown(self):
        body = self.body
        return mark_safe(markdown(body))

class Blog_Comment(models.Model):
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.body[:100]
