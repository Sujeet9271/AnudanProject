from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
from django.forms import fields
from .models import FiscalYear, MunicipalityStaff, PalikaUser, Profile
from Anudan.models import Municipality
from django.utils.translation import gettext as _



class LoginForm(forms.ModelForm):

    email = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['email', 'password']  

class OTP(forms.Form):

    otp = forms.IntegerField()

    class Meta:
        fields = ['otp']        

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label=_('email'))
    
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
    municipality = forms.ModelChoiceField(queryset=Municipality.objects.none())
    user = forms.ModelChoiceField(PalikaUser.objects.none())

    def __init__(self,*args,**kwargs):
        super(PalikaStaffForm,self).__init__(*args,**kwargs)        
        self.fields['municipality'].queryset = Municipality.objects.all().filter(id=self.current_user.municipality_staff.municipality.id) if not self.current_user.is_superuser else Municipality.objects.all()
        self.fields['municipality'].initial = Municipality.objects.get(id = self.current_user.municipality_staff.municipality.id) if not self.current_user.is_superuser else None
        self.fields['user'].queryset = PalikaUser.objects.all() if self.current_user.is_superuser else PalikaUser.objects.all().filter(municipality_staff__municipality=self.current_user.municipality_staff.municipality)
        

    class Meta:
        model = MunicipalityStaff
        fields = ['municipality','user']


class ProfileForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=PalikaUser.objects.none())
    address = forms.CharField()
    contact_number = forms.IntegerField()

    def __init__(self,*args,**kwargs):
        super(ProfileForm,self).__init__(*args,**kwargs)
        self.fields['user'].queryset = PalikaUser.objects.all().filter(id=self.current_user.id) if  not self.current_user.is_superuser else PalikaUser.objects.all()


    class Meta:
        model = Profile
        fields = ['user','address','contact_number']

class FiscalYearForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date    = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = FiscalYear
        fields = ['start_date','end_date']

