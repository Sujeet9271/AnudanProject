from re import template
from django.http.response import HttpResponse
from Municipality.models import Municipality
from django.contrib import admin
from .models import AnudanCompany, Karyakram, MedicineRequest,Samagri,AnudanPersonal, Unit
from django.utils.translation import gettext_lazy as _
from .forms import AnudanCompanyForm,AnudanPersonalForm,KaryakramForm
import csv
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

# Register your models here.



@admin.register(MedicineRequest)
class MedicineRequestAdmin(admin.ModelAdmin):
    list_display = ['id','name','ward','tole','medicine','quantity']
    list_filter = ['ward','tole','medicine']


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(municipality = request.user.municipality_staff.municipality.id)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'municipality':
            kwargs['queryset'] = Municipality.objects.filter(id = request.user.municipality_staff.municipality.id) if not request.user.is_superuser else Municipality.objects.all()
            kwargs['initial'] = Municipality.objects.get(id = request.user.municipality_staff.municipality.id) if not request.user.is_superuser else None
        return super(MedicineRequestAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


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

@admin.action(permissions=['change'],description='Approve Selected')
def approve(modaladmin,request, queryset):
    queryset.update(approval='Approved')

@admin.action(permissions=['change'],description='Disapprove Selected')
def disapprove(modaldamin,request, queryset):
    queryset.update(approval='Not Approved')

@admin.register(AnudanPersonal)
class AnudanPersonalAdmin(admin.ModelAdmin):
    list_display=['id','name','municipality','ward','tole','karyakram','samagri','approval']
    list_filter=['approval','ward','tole','jari_jilla','karyakram']
    list_display_links=['id','name']
    actions = [approve,disapprove,'export_to_csv']
    ordering=['ward']
    list_editable=['approval']


    fieldsets = (
        (_('Fiscal Year'),{'fields':('fiscal_year',),'classes':('wide',)}),
        (_('Municipality'), {'fields': ('municipality',),'classes':("wide",),'description':'Select Municipality'}),
        (_('Personal info'), {'fields': ( 'name',),'classes':("wide",),'description':'Enter Your Name'}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':'Enter Your Address'}),
        (_('Nagrikta Details'), {'fields': ('nagrikta_number', 'jari_jilla','nagrikta_front','nagrikta_back'),'classes':("wide",),'description':'Enter your citizenship details'}),
        (_('Anudan Request'),{'fields':('sector','karyakram','samagri','quantity'),'classes':("wide",),'description':'Select karyakram and its respective samagri'}),
        (_('Approval'),{'fields':('approval',),'classes':("wide",),'description':'Test'})

    )


    add_fieldsets = (
        (_('Fiscal Year'),{'fields':('fiscal_year',),'classes':('wide',)}),
        (_('Municipality'), {'fields': ('municipality',),'classes':("wide",),'description':'Select Municipality'}),
        (_('Personal info'), {'fields': ( 'name',),'classes':("wide",),'description':'Enter Your Name'}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':'Enter Your Address'}),
        (_('Nagrikta Details'), {'fields': ('nagrikta_number', 'jari_jilla','nagrikta_front','nagrikta_back'),'classes':("wide",),'description':'Enter your citizenship details'}),
        (_('Anudan Request'),{'fields':('sector','karyakram','samagri','quantity'),'classes':("wide",),'description':'Select karyakram and its respective samagri'}),

    )

    staff_fieldsets = (
        (_('Municipality'), {'fields': ('municipality',),'classes':("collapse",)}),
        (_('Fiscal Year'),{'fields':('fiscal_year',),'classes':('wide',)}),        
        (_('Personal info'), {'fields': ( 'name',),'classes':("wide",),'description':'Enter Your Name'}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':'Enter Your Address'}),
        (_('Nagrikta Details'), {'fields': ('nagrikta_number', 'jari_jilla','nagrikta_front','nagrikta_back'),'classes':("wide",),'description':'Enter your citizenship details'}),
        (_('Anudan Request'),{'fields':('sector','karyakram','samagri','quantity'),'classes':("wide",),'description':'Select karyakram and its respective samagri'}),

    )

    @admin.action(description='Export to CSV')
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="books.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name','Municipality','Tole','Ward', 'Karyakram', 'Samagri', 'Quantity','Approval'])
        books = queryset.values_list('name','municipality__name','ward','tole','karyakram__name', 'samagri__name', 'quantity', 'approval')
        for book in books:
            writer.writerow(book)
        return response

    def get_queryset(self, request):
        qs = super(AnudanPersonalAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(municipality=request.user.municipality_staff.municipality)


    def get_form(self, request,*args, **kwargs):        
        form = AnudanPersonalForm
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
        return self.add_fieldsets if request.user.is_superuser else self.staff_fieldsets

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return self.list_filter+['municipality']
        return self.list_filter



    

@admin.register(AnudanCompany)
class AnudanCompanyAdmin(admin.ModelAdmin):
    list_display=['firm_name','registration_no','pan_no','vat_no','ward','tole','registered_place','municipality','approval']
    list_display_links=['firm_name','registration_no','pan_no','vat_no']
    list_filter=['approval','ward','tole','fiscal_year']
    actions=[approve,disapprove,'export_to_csv','render_pdf_view']
    form = AnudanCompanyForm
    

    fieldsets = (
        (_('Fiscal Year'),{'fields':('fiscal_year',)}),
        (_('Nagar Palika'), {'fields': ('municipality',),'classes':("wide",),'description':'Select Nagar Palika'}),
        (_('Firm info'), {'fields': ( 'firm_name','pan_no','vat_no','registration_no','registered_place','firm_registration_proof','anya_darta'),'classes':("wide",),'description':'About Firm'}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':'Enter Your Address'}),
        (_('Anudan Request'),{'fields':('ward_sifaris','prastavan'),'classes':("wide",),'description':'Select karyakram and its respective samagri'}),
        (_('Approval'),{'fields':('approval',),'classes':("wide",),'description':'Test'})
    )


    add_fieldsets = (
        (_('Fiscal Year'),{'fields':('fiscal_year',)}),
        (_('Nagar Palika'), {'fields': ('municipality'),'classes':("wide",),'description':'Select Nagar Palika'}),
        (_('Firm info'), {'fields': ( 'firm_name','pan_no','vat_no','registration_no','registered_place','firm_registration_proof','anya_darta'),'classes':("wide",),'description':'About Firm'}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':'Enter Your Address'}),
        (_('Anudan Request'),{'fields':('ward_sifaris','prastavan'),'classes':("wide",),'description':'Select karyakram and its respective samagri'}),
    )

    staff_fieldsets = (
        (_('Nagar Palika'), {'fields': ('municipality',),'classes':("collapse",),'description':'Select Nagar Palika'}),
        (_('Fiscal Year'),{'fields':('fiscal_year',)}),
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

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return self.list_filter+['municipality']
        return self.list_filter

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
        return self.staff_fieldsets if not request.user.is_superuser else self.add_fieldsets


    @admin.action(description='Export to csv')
    def export_to_csv(self, request, queryset):        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="AnudanCompany.csv"'
        writer = csv.writer(response)
        if 'ne' in request.path:
            writer.writerow(['नाम','नगरपालिका','टोल','वडा','वडा सिफरिस','प्रस्तावना'])
        else:
            writer.writerow(['Name','Municipality','Tole','Ward','Ward Sifaris','Prastavan'])
        books = queryset.values_list('firm_name','municipality__name','ward','tole','ward_sifaris', 'prastavan')
        for book in books:
            writer.writerow(book)
        return response

    @admin.action(description='Export to pdf')
    def render_pdf_view(self,request,queryset):
        template_path = 'pdf-output.html'
        context = {'queryset': queryset}
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="AnudanCompany.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response