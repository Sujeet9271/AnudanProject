from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
from django.forms import fields
from .models import PalikaUser, Profile 

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = PalikaUser
        fields = ("email","username","password1","password2",)

    def save(self,commit = True):
        user = super(CustomUserCreationForm,self).save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = PalikaUser
        fields = ('email','username','first_name','last_name',)

