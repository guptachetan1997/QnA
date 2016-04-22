from django import forms
from models import UserProfile

class UserProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(2016,1939,-1), attrs={'class':"form-control", 'required':''}))
    class Meta:
        model = UserProfile
        fields = ('gender', 'bio', 'dob', 'city', 'education', 'workplace', 'profile_pic')
        exclude = ('user', )
        widgets = {
            'gender' : forms.TextInput(attrs = {'class': "form-control", 'maxlength':1, 'required':'', 'autofocus':'', 'placeholder': 'Gender'}),
            'bio' : forms.TextInput(attrs = {'class': "form-control", 'maxlength':100, 'placeholder': 'Bio'}),
            'city' : forms.TextInput(attrs = {'class': "form-control", 'maxlength':50, 'placeholder': 'City'}),
            'education' : forms.TextInput(attrs = {'class': "form-control", 'maxlength':100, 'placeholder': 'Education'}),
            'workplace' : forms.TextInput(attrs = {'class': "form-control", 'maxlength':100, 'placeholder': 'Workplace'}),
        }
