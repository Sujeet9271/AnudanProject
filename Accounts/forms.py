from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import PalikaUser 

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