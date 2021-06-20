from django import forms
from .models import AnudanCompany, AnudanPersonal,Karyakram, Municipality,Samagri
from django.utils.translation import ugettext_lazy as _

class AnudanPersonalForm(forms.ModelForm):
    municipality = forms.ModelChoiceField(label=_('Municipality'),queryset=Municipality.objects.none())
    

    def __init__(self, *args,**kwargs):
        super(AnudanPersonalForm,self).__init__(*args,**kwargs)
        self.fields['municipality'].queryset = Municipality.objects.filter(id=self.current_user.palika_staff.municipality.id) if not self.current_user.is_superuser else Municipality.objects.all()

    class Meta:
        model = AnudanPersonal
        fields = ['municipality','name','ward','tole','nagrikta_number','jari_jilla','nagrikta_front','nagrikta_back','karyakram','samagri']



class AnudanCompanyForm(forms.ModelForm):
    municipality = forms.ModelChoiceField(label=_('Municipality'),queryset=Municipality.objects.none())

    def __init__(self, *args,**kwargs):
        super(AnudanCompanyForm,self).__init__(*args,**kwargs)
        self.fields['municipality'].queryset = Municipality.objects.filter(id=self.current_user.palika_staff.municipality.id) if not self.current_user.is_superuser else Municipality.objects.all()


    class Meta:
        model = AnudanCompany
        fields = '__all__'



class KaryakramForm(forms.ModelForm):
    municipality = forms.ModelChoiceField(label=_('Municipality'),queryset=Municipality.objects.none())

    def __init__(self, *args,**kwargs):
        super(KaryakramForm,self).__init__(*args,**kwargs)
        self.fields['municipality'].queryset = Municipality.objects.filter(id=self.current_user.palika_staff.municipality.id) if not self.current_user.is_superuser else Municipality.objects.all()

    class Meta:
        model = Karyakram
        fields = ['municipality','name']

    

class SamagriForm(forms.ModelForm):
    municipality = forms.ModelChoiceField(label=_('Municipality'),queryset=Municipality.objects.none())

    def __init__(self, *args,**kwargs):
        super(SamagriForm,self).__init__(*args,**kwargs)
        self.fields['municipality'].queryset = Municipality.objects.filter(id=self.current_user.palika_staff.municipality.id) if not self.current_user.is_superuser else Municipality.objects.all()

    class Meta:
        model = Samagri
        fields = ['municipality','karyakram','name']

    
