from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

from .models import Profile,Group,Task

class SignupForm(UserCreationForm):
    email=forms.EmailField()

    class Meta:
        model=User
        fields=['username','email','password1','password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput)
         
class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['firstname','lastname','email','phone','address']



class GroupForm(forms.ModelForm):
    class Meta:
        model=Group
        fields=['name']



class TaskAssignForm(forms.ModelForm):
    class  Meta:
        model=Task
        fields=['group','assigned_to','title','description','deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={
                'type': 'date',   # ✅ HTML5 calendar input
                'class': 'form-control',  # optional Bootstrap class
            }),
        }






class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['uploaded_file','user_description']
 