from django.contrib import admin
from .models import AnudanCompany, Karyakram,Samagri,AnudanPersonal,Municipality
from django.utils.translation import gettext as _
from .forms import AnudanPersonalForm,KaryakramForm,SamagriForm,AnudanCompanyForm
# Register your models here.



@admin.register(Municipality)
class NagarPalikaAdmin(admin.ModelAdmin):
    list_display=['id','name','contact_number']
    list_display_links=['id','name',]

class SamagriInline(admin.StackedInline):
    model = Samagri
    extra = 1


@admin.register(Karyakram)
class KaryakramAdmin(admin.ModelAdmin):
    list_display=['id','name','municipality']
    list_display_links=['id','name']
    list_filter=['municipality']
    form=KaryakramForm

    def get_queryset(self, request):
        qs = super(KaryakramAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(municipality=request.user.palika_staff.municipality)

    
    def get_form(self, request,*args, **kwargs):
        form = super(KaryakramAdmin,self).get_form(request,*args, **kwargs)
        form.current_user=request.user
        return form


@admin.register(Samagri)
class SamagriAdmin(admin.ModelAdmin):
    list_display=['id','name','karyakram']
    list_filter=['karyakram','municipality']
    list_display_links=['id','name']
    form = SamagriForm

    def get_queryset(self, request):
        qs = super(SamagriAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(municipality=request.user.palika_staff.municipality)

    
    def get_form(self, request,*args, **kwargs):
        form = super(SamagriAdmin,self).get_form(request,*args, **kwargs)
        form.current_user=request.user
        return form

    



@admin.register(AnudanPersonal)
class AnudanPersonalAdmin(admin.ModelAdmin):
    list_display=['id','name','ward','tole','nagrikta_number','jari_jilla','karyakram','nagrikta_front','nagrikta_back','samagri','municipality','approval']
    list_filter=['approval','ward','tole','jari_jilla','karyakram','samagri']
    list_display_links=['id','name']
    form = AnudanPersonalForm


    fieldsets = (

        (_('Municipality'), {'fields': ('municipality',),'classes':("wide",),'description':'Select Municipality'}),
        (_('Personal info'), {'fields': ( 'name',),'classes':("wide",),'description':'Enter Your Name'}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':'Enter Your Address'}),
        (_('Nagrikta Details'), {'fields': ('nagrikta_number', 'jari_jilla','nagrikta_front','nagrikta_back'),'classes':("wide",),'description':'Enter your citizenship details'}),
        (_('Anudan Request'),{'fields':('karyakram','samagri'),'classes':("wide",),'description':'Select karyakram and its respective samagri'}),
        (_('Approval'),{'fields':('approval',),'classes':("wide",),'description':'Test'})

    )


    add_fieldsets = (

        (_('Municipality'), {'fields': ('municipality',),'classes':("wide",),'description':'Select Municipality'}),
        (_('Personal info'), {'fields': ( 'name',),'classes':("wide",),'description':'Enter Your Name'}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':'Enter Your Address'}),
        (_('Nagrikta Details'), {'fields': ('nagrikta_number', 'jari_jilla','nagrikta_front','nagrikta_back'),'classes':("wide",),'description':'Enter your citizenship details'}),
        (_('Anudan Request'),{'fields':('karyakram','samagri'),'classes':("wide",),'description':'Select karyakram and its respective samagri'}),

    )

    def get_queryset(self, request):
        qs = super(AnudanPersonalAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(municipality=request.user.palika_staff.municipality)


    def get_form(self, request,*args, **kwargs):
        form = super(AnudanPersonalAdmin,self).get_form(request,*args, **kwargs)
        form.current_user=request.user
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if request.user.is_superuser or request.user.is_admin:
                return self.readonly_fields 
            else:
                return self.readonly_fields+('approval',) # editing an existing object

        if request.user.is_superuser or request.user.is_admin:
            return self.readonly_fields 
        else:
            return self.readonly_fields+('approval',)

    def get_fieldsets(self, request, obj):
        if obj:
            return self.fieldsets
        return self.add_fieldsets

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return self.list_filter+['municipality']
        return self.list_filter
        


    


@admin.register(AnudanCompany)
class AnudanCompanyAdmin(admin.ModelAdmin):
    list_display=['firm_name','registration_no','pan_no','vat_no','ward','tole','registered_place','municipality','approval']
    list_display_links=['firm_name','registration_no','pan_no','vat_no']
    list_filter=['approval','ward','tole','municipality']
    form = AnudanCompanyForm
    

    fieldsets = (

        (_('Municipality'), {'fields': ('municipality',),'classes':("wide",),'description':_('Select Municipality')}),
        (_('Firm info'), {'fields': ( 'firm_name','pan_no','vat_no','registration_no','registered_place','firm_registration_proof'),'classes':("wide",),'description':'About Firm'}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':'Enter Your Address'}),
        (_('Anudan Request'),{'fields':('ward_sifaris','prastavan'),'classes':("wide",),'description':'Select karyakram and its respective samagri'}),
        (_('Approval'),{'fields':('approval',),'classes':("wide",),'description':'Test'})
    )


    add_fieldsets = (

        (_('Municipality'), {'fields': ('municipality',),'classes':("wide",),'description':'Select Municipality'}),
        (_('Firm info'), {'fields': ( 'firm_name','pan_no','vat_no','registration_no','registered_place','firm_registration_proof'),'classes':("wide",),'description':'About Firm'}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':'Enter Your Address'}),
        (_('Anudan Request'),{'fields':('ward_sifaris','prastavan'),'classes':("wide",),'description':'Select karyakram and its respective samagri'}),
    )

    def get_queryset(self, request):
        qs = super(AnudanCompanyAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(municipality=request.user.palika_staff.municipality)

    def get_form(self, request,*args, **kwargs):
        form = super(AnudanCompanyAdmin,self).get_form(request,*args, **kwargs)
        form.current_user=request.user
        return form

    def get_readonly_fields(self, request, obj=None):
        if obj:
            if request.user.is_superuser or request.user.is_admin:
                return self.readonly_fields 
            else:
                return self.readonly_fields+('approval',) # editing an existing object

        if request.user.is_superuser or request.user.is_admin:
            return self.readonly_fields 
        else:
            return self.readonly_fields+('approval',)


    def get_fieldsets(self, request, obj):
        if obj:
            return self.fieldsets
        return self.add_fieldsets