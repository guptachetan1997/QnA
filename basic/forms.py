from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class' : "form-control", 'maxlength' : 255, 'required': '', 'autofocus':'', 'placeholder' : 'Username'}),
            'first_name': forms.TextInput(attrs={'class' : "form-control", 'maxlength' : 255, 'required': '', 'placeholder' : 'First Name'}),
            'last_name': forms.TextInput(attrs={'class' : "form-control", 'maxlength' : 255, 'required': '', 'placeholder' : 'Last Name'}),
            'email': forms.TextInput(attrs={'class' : "form-control", 'maxlength' : 255, 'required': '', 'placeholder' : 'Email'}),
            'password': forms.PasswordInput(attrs={'class' : "form-control", 'maxlength' : 255, 'required': '', 'placeholder' : 'Password'}),

        }

    def save(self, commit=True):
        user = super(ModelForm,self).save(commit = False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
