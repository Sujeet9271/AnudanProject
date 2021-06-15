from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
from .models import PalikaStaff, PalikaUser, Profile
from Anudan.models import NagarPalika

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

class PalikaStaffForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(PalikaStaffForm,self).__init__(*args,**kwargs)
        self.fields['palika'].queryset = NagarPalika.objects.all().filter(id=self.current_user.palika_staff.palika.id) if not self.current_user.is_superuser else NagarPalika.objects.all()
        self.fields['user'].queryset = PalikaUser.objects.all() if self.current_user.is_superuser else PalikaUser.objects.all().filter(palika_staff__palika=self.current_user.palika_staff.palika)
        

    class Meta:
        model = PalikaStaff
        fields = ['palika','user']


    # def clean(self):
    #     return super().clean()

class ProfileForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(ProfileForm,self).__init__(*args,**kwargs)
        self.fields['user'].queryset = PalikaUser.objects.all().filter(id=self.current_user.id)


    class Meta:
        model = Profile
        fields = ['user','address','contact_number']


