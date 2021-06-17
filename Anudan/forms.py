from django import forms
from .models import AnudanCompany, AnudanPersonal,Karyakram, NagarPalika,Samagri

class AnudanPersonalForm(forms.ModelForm):
    nagarpalika = forms.ModelChoiceField(queryset=NagarPalika.objects.none())
    

    def __init__(self, *args,**kwargs):
        super(AnudanPersonalForm,self).__init__(*args,**kwargs)
        self.fields['nagarpalika'].queryset = NagarPalika.objects.filter(id=self.current_user.palika_staff.palika.id) if not self.current_user.is_superuser else NagarPalika.objects.all()

    class Meta:
        model = AnudanPersonal
        fields = ['nagarpalika','name','ward','tole','nagrikta_number','jari_jilla','nagrikta_front','nagrikta_back','karyakram','samagri']



class AnudanCompanyForm(forms.ModelForm):
    nagarpalika = forms.ModelChoiceField(queryset=NagarPalika.objects.none())

    def __init__(self, *args,**kwargs):
        super(AnudanCompanyForm,self).__init__(*args,**kwargs)
        self.fields['nagarpalika'].queryset = NagarPalika.objects.filter(id=self.current_user.palika_staff.palika.id) if not self.current_user.is_superuser else NagarPalika.objects.all()


    class Meta:
        model = AnudanCompany
        fields = '__all__'



class KaryakramForm(forms.ModelForm):
    nagarpalika = forms.ModelChoiceField(queryset=NagarPalika.objects.none())

    def __init__(self, *args,**kwargs):
        super(KaryakramForm,self).__init__(*args,**kwargs)
        self.fields['nagarpalika'].queryset = NagarPalika.objects.filter(id=self.current_user.palika_staff.palika.id) if not self.current_user.is_superuser else NagarPalika.objects.all()

    class Meta:
        model = Karyakram
        fields = ['nagarpalika','name']

    

class SamagriForm(forms.ModelForm):
    nagarpalika = forms.ModelChoiceField(queryset=NagarPalika.objects.none())

    def __init__(self, *args,**kwargs):
        super(SamagriForm,self).__init__(*args,**kwargs)
        self.fields['nagarpalika'].queryset = NagarPalika.objects.filter(id=self.current_user.palika_staff.palika.id) if not self.current_user.is_superuser else NagarPalika.objects.all()

    class Meta:
        model = Samagri
        fields = ['nagarpalika','karyakram','name']

    
