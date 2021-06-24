from django.contrib import admin
from .models import AnudanCompany, Karyakram,Samagri,AnudanPersonal,Municipality, Unit
from django.utils.translation import gettext_lazy as _
from .forms import AnudanCompanyForm,AnudanPersonalForm,KaryakramForm
from django.http import HttpResponse
import csv

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
    inlines=[SamagriInline]
    form=KaryakramForm

    def get_queryset(self, request):
        qs = super(KaryakramAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(municipality=request.user.municipality_staff.municipality)

    
    def get_form(self, request,*args, **kwargs):
        form = super(KaryakramAdmin,self).get_form(request,*args, **kwargs)
        form.current_user=request.user
        return form

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    

# @admin.register(Samagri)
# class SamagriAdmin(admin.ModelAdmin):
#     list_display=['id','name','karyakram',]
#     list_filter=['karyakram']
#     list_display_links=['id','name']
#     form = SamagriForm
    

#     def get_queryset(self, request):
#         qs = super(SamagriAdmin, self).get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(municipality=request.user.municipality_staff.municipality)

    
    # def get_form(self, request,*args, **kwargs):
    #     form = super(SamagriAdmin,self).get_form(request,*args, **kwargs)
    #     form.current_user=request.user
    #     return form

@admin.action(permissions=['change'])
def approve(self, request, queryset):
    queryset.update(approval='Approved')
approve.short_description = 'Approve'

@admin.action(permissions=['change'])
def disapprove(self, request, queryset):
    queryset.update(approval='Not Approved')
disapprove.short_description = 'Disapprove'

@admin.register(AnudanPersonal)
class AnudanPersonalAdmin(admin.ModelAdmin):
    list_display=['id','name','municipality','ward','tole','karyakram','samagri','approval']
    list_filter=['approval','ward','tole','jari_jilla','karyakram']
    list_display_links=['id','name']
    form = AnudanPersonalForm
    actions = ["approve","disapprove","export_to_csv"]
    ordering=['ward']
    list_editable=['approval']


    fieldsets = (
        (_('Fiscal Year'),{'fields':('fiscal_year',),'classes':('wide',)}),
        (_('Municipality'), {'fields': ('municipality',),'classes':("wide",),'description':'Select Municipality'}),
        (_('Personal info'), {'fields': ( 'name',),'classes':("wide",),'description':'Enter Your Name'}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':'Enter Your Address'}),
        (_('Nagrikta Details'), {'fields': ('nagrikta_number', 'jari_jilla','nagrikta_front','nagrikta_back'),'classes':("wide",),'description':'Enter your citizenship details'}),
        (_('Anudan Request'),{'fields':('karyakram','samagri','quantity'),'classes':("wide",),'description':'Select karyakram and its respective samagri'}),
        (_('Approval'),{'fields':('approval',),'classes':("wide",),'description':'Test'})

    )


    add_fieldsets = (
        (_('Fiscal Year'),{'fields':('fiscal_year',),'classes':('wide',)}),
        (_('Municipality'), {'fields': ('municipality',),'classes':("wide",),'description':'Select Municipality'}),
        (_('Personal info'), {'fields': ( 'name',),'classes':("wide",),'description':'Enter Your Name'}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':'Enter Your Address'}),
        (_('Nagrikta Details'), {'fields': ('nagrikta_number', 'jari_jilla','nagrikta_front','nagrikta_back'),'classes':("wide",),'description':'Enter your citizenship details'}),
        (_('Anudan Request'),{'fields':('karyakram','samagri','quantity'),'classes':("wide",),'description':'Select karyakram and its respective samagri'}),

    )



    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="books.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name','Municipality','Tole','Ward', 'Karyakram', 'Samagri', 'Quantity','Approval'])
        books = queryset.values_list('name','municipality__name','ward','tole','karyakram__name', 'samagri__name', 'quantity', 'approval')
        for book in books:
            writer.writerow(book)
        return response
    export_to_csv.short_description = 'Export to csv'

    def get_queryset(self, request):
        qs = super(AnudanPersonalAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(municipality=request.user.municipality_staff.municipality)


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
        (_('Fiscal Year'),{'fields':('fiscal_year',),'classes':('wide',)}),

        (_('Nagar Palika'), {'fields': ('municipality',),'classes':("wide",),'description':'Select Nagar Palika'}),
        (_('Firm info'), {'fields': ( 'firm_name','pan_no','vat_no','registration_no','registered_place','firm_registration_proof','anya_darta'),'classes':("wide",),'description':'About Firm'}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':'Enter Your Address'}),
        (_('Anudan Request'),{'fields':('ward_sifaris','prastavan'),'classes':("wide",),'description':'Select karyakram and its respective samagri'}),
        (_('Approval'),{'fields':('approval',),'classes':("wide",),'description':'Test'})
    )


    add_fieldsets = (
        (_('Fiscal Year'),{'fields':('fiscal_year',),'classes':('wide',)}),

        (_('Nagar Palika'), {'fields': ('municipality',),'classes':("wide",),'description':'Select Nagar Palika'}),
        (_('Firm info'), {'fields': ( 'firm_name','pan_no','vat_no','registration_no','registered_place','firm_registration_proof','anya_darta'),'classes':("wide",),'description':'About Firm'}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':'Enter Your Address'}),
        (_('Anudan Request'),{'fields':('ward_sifaris','prastavan'),'classes':("wide",),'description':'Select karyakram and its respective samagri'}),
    )

    def get_queryset(self, request):
        qs = super(AnudanCompanyAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(municipality=request.user.municipality_staff.municipality)

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
