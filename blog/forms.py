from django import forms
from .models import Post,Blog_Comment
from pagedown.widgets import PagedownWidget

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=PagedownWidget())
    class Meta:
        model = Post
        fields = ('title', 'body')
        exclude = ('date',)
        widgets = {
            # 'body' : forms.Textarea(attrs = {'class': "form-control input-large", 'required':'', 'placeholder': 'Post'}),
            'title' : forms.TextInput(attrs = {'class': "form-control", 'maxlength':255, 'required':'', 'autofocus':'', 'placeholder': 'Title'}),
        }

class AddComment(forms.ModelForm):
    class Meta:
        model = Blog_Comment
        fields = ('body', )
        exclude = ('name', 'date', 'post',)
        widgets = {
            'body' : forms.TextInput(attrs = {'class': "form-control", 'maxlength':255, 'placeholder': 'Comment'}),
        }
