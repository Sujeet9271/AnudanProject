from django import forms
from .models import AnudanCompany, AnudanPerosnal,Karyakram, NagarPalika,Samagri

class AnudanPersonalForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        super(AnudanPersonalForm,self).__init__(*args,**kwargs)
        self.fields['nagarpalika'].queryset = NagarPalika.objects.all().filter(id=self.current_user.palika_staff.palika.id) if not self.current_user.is_superuser else NagarPalika.objects.all()


    class Meta:
        model = AnudanPerosnal
        fields = ['nagarpalika','name','ward','tole','nagrikta_number','jari_jilla','nagrikta_front','nagrikta_back','karyakram','samagri']



class AnudanCompanyForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        super(AnudanCompanyForm,self).__init__(*args,**kwargs)
        self.fields['nagarpalika'].queryset = NagarPalika.objects.all().filter(id=self.current_user.palika_staff.palika.id) if not self.current_user.is_superuser else NagarPalika.objects.all()


    class Meta:
        model = AnudanCompany
        fields = '__all__'



class KaryakramForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        super(KaryakramForm,self).__init__(*args,**kwargs)
        self.fields['nagarpalika'].queryset = NagarPalika.objects.all().filter(id=self.current_user.palika_staff.palika.id) if not self.current_user.is_superuser else NagarPalika.objects.all()

    class Meta:
        model = Karyakram
        fields = ['nagarpalika','name']

    

class SamagriForm(forms.ModelForm):

    def __init__(self, *args,**kwargs):
        super(SamagriForm,self).__init__(*args,**kwargs)
        self.fields['nagarpalika'].queryset = NagarPalika.objects.all().filter(id=self.current_user.palika_staff.palika.id) if not self.current_user.is_superuser else NagarPalika.objects.all()
        self.fields['karyakram'].queryset = Karyakram.objects.all().filter(nagarpalika=self.current_user.palika_staff.palika.id) if not self.current_user.is_superuser else Karyakram.objects.all()

    class Meta:
        model = Samagri
        fields = ['nagarpalika','karyakram','name']

    
