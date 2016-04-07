from django import forms
from django.forms import ModelForm
from models import Question,Answer,Comment
from pagedown.widgets import PagedownWidget

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['date', 'upvotes', 'user', 'ans_count']
        fields = ('q_text', 'q_body' , 'anonymous', 'tags')
        widgets = {
            'q_text': forms.TextInput(attrs={'class' : "form-control", 'maxlength' : 200, 'required': '', 'autofocus':'', 'placeholder' : 'Question'}),
            'q_body': forms.Textarea(attrs={'class' : "form-control input-large", 'placeholder' : 'Additional details!'}),
            'tags': forms.TextInput(attrs={'class' : "form-control", 'maxlength' : 200, 'placeholder' : 'Tags'}),
            'anonymous' : forms.CheckboxInput(attrs = {'placeholder':"Anonymous"}),
        }

class AnswerForm(forms.ModelForm):
    ans_text = forms.CharField(widget=PagedownWidget)
    class Meta:
        model = Answer
        exclude = ['timestamp', 'upvotes', 'downvotes', 'question', 'user']
        fields = ('ans_text', 'anonymous')
        widgets = {
            # 'ans_text': forms.Textarea(attrs={'class' : "form-control input-large", 'required': '', 'autofocus':'', 'placeholder' : 'Your answer!'}),
            'anonymous' : forms.CheckboxInput(attrs = {'placeholder':"Anonymous"}),
        }

class AddComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        exclude = ('timestamp', 'answer', 'user',)
        widgets = {
            'body' : forms.TextInput(attrs = {'class': "form-control", 'placeholder': 'Comment'}),
        }
