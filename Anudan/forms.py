from django import forms
from .models import AnudanCompany, AnudanPersonal,Karyakram,Samagri
from django.utils.translation import gettext_lazy as _
from Accounts.models import FiscalYear
from Municipality.models import Municipality,Sector


class AnudanPersonalForm(forms.ModelForm):
    municipality = forms.ModelChoiceField(label=_('Municipality'),queryset=Municipality.objects.none())
    quantity = forms.IntegerField(label = _('Quantity'))
    fiscal_year = forms.ModelChoiceField(label=_('Fiscal Year'),queryset=FiscalYear.objects.all())
      

    def __init__(self, *args,**kwargs):
        super(AnudanPersonalForm,self).__init__(*args,**kwargs)
        self.fields['municipality'].queryset = Municipality.objects.filter(id = self.current_user.municipality_staff.municipality.id) if not self.current_user.is_superuser else Municipality.objects.all()
        self.fields['municipality'].initial  = Municipality.objects.get(id=self.current_user.municipality_staff.municipality.id) if not self.current_user.is_superuser else None
    
    class Meta:
        model = AnudanPersonal
        fields = ['fiscal_year','municipality','name','ward','tole','nagrikta_number','jari_jilla','nagrikta_front','nagrikta_back','sector','karyakram','samagri','quantity']


        



# class AnudanCompanyForm(forms.ModelForm):
#     fiscal_year = forms.ModelChoiceField(label=_('Fiscal Year'),queryset=FiscalYear.objects.all())
#     municipality = forms.ModelChoiceField(queryset=Municipality.objects.none(),label=_('Municipality'))
    
    

#     def __init__(self, *args,**kwargs):
#         super(AnudanCompanyForm,self).__init__(*args,**kwargs)
#         self.fields['municipality'].queryset = Municipality.objects.filter(id = self.current_user.municipality_staff.municipality.id) if not self.current_user.is_superuser else Municipality.objects.all()
#         self.fields['municipality'].initial = Municipality.objects.get(id = self.current_user.municipality_staff.municipality.id) if not self.current_user.is_superuser else None


#     class Meta:
#         model = AnudanCompany
#         fields = ['fiscal_year','municipality','firm_name','vat_no','pan_no','registration_no','ward','tole','registered_place','firm_registration_proof','anya_darta','ward_sifaris','prastavan','approval']


class KaryakramForm(forms.ModelForm):
    municipality = forms.ModelChoiceField(label=_('Municipality'),queryset=Municipality.objects.none(),initial=0)    

    def __init__(self, *args,**kwargs):
        super(KaryakramForm,self).__init__(*args,**kwargs)
        self.fields['municipality'].queryset = Municipality.objects.filter(id=self.current_user.municipality_staff.municipality.id) if not self.current_user.is_superuser else Municipality.objects.all()
        self.fields['municipality'].initial  = 0 if not self.current_user.is_superuser else None
        
    class Meta:
        model = Karyakram
        fields = ['municipality','sector','name']

    

class SamagriForm(forms.ModelForm):

    class Meta:
        model = Samagri
        fields = ['karyakram','name']

    
class AnudanCompanyForm(forms.ModelForm):
    municipality = forms.ModelChoiceField(queryset=Municipality.objects.none())
    fiscal_year = forms.ModelChoiceField(queryset=FiscalYear.objects.all())

    def __init__(self, *args,**kwargs):
        super(AnudanCompanyForm,self).__init__(*args,**kwargs)
        self.fields['municipality'].queryset = Municipality.objects.filter(id = self.current_user.municipality_staff.municipality.id) if not self.current_user.is_superuser else Municipality.objects.all()
        self.fields['municipality'].initial = Municipality.objects.get(id = self.current_user.municipality_staff.municipality.id) if not self.current_user.is_superuser else None


    class Meta:
        model = AnudanCompany
        fields = '__all__'

