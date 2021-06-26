from re import template
from django.http.response import HttpResponse
from Municipality.models import Municipality
from django.contrib import admin
from .models import AnudanCompany, Karyakram, Medicine, MedicineRequest, MedicineRequested,Samagri,AnudanPersonal, Unit
from django.utils.translation import gettext_lazy as _
from .forms import AnudanCompanyForm,AnudanPersonalForm,KaryakramForm
import csv
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

# Register your models here.
@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display=['id','name']

class MedicineInline(admin.TabularInline):
    model = MedicineRequested
    extra = 1


@admin.register(MedicineRequest)
class MedicineRequestAdmin(admin.ModelAdmin):
    list_display = ['id','name','ward','tole']
    list_display_links=['id','name']
    list_filter = ['ward','tole']
    inlines=[MedicineInline]
    actions=['export_to_csv','render_pdf_view']

    @admin.action(description='Export to CSV')
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="MedicineRequests.csv"'
        print(request.path)
        writer = csv.writer(response)
        if '/ne/' in request.path:
            writer.writerow(['नाम','सम्पर्क नम्बर','नगरपालिका','वडा','टोल','औषधी','मात्रा'])
        else:
            writer.writerow(['Name','Contact Number','Municipality','Ward','Tole','Medicines','Quantity'])
        id = queryset.values_list('id',flat=True)
        for id in id:
            records=MedicineRequested.objects.filter(requested_by__id=id).values_list('requested_by__name','requested_by__contact_number','requested_by__municipality__name','requested_by__ward__name','requested_by__tole','medicine__name','quantity')
            for record in records:
                writer.writerow(record)
        return response

    @admin.action(description='Export to pdf')
    def render_pdf_view(self,request,queryset):
        template_path = 'MedicineRequest.html'
        id = [id for id in queryset.values_list('id',flat=True)]
        medicines =MedicineRequested.objects.filter(requested_by__id__in=id).order_by('id')
        context = {'queryset': medicines}
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="MedicineRequest.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response


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
    list_filter=['fiscal_year','sector','karyakram','ward','approval']
    list_display_links=['id','name']
    actions = [approve,disapprove,'export_to_csv','render_pdf_view']
    ordering=['ward']
    list_editable=['approval']


    fieldsets = (
        (_('Fiscal Year'),{'fields':('fiscal_year',),'classes':('wide',)}),
        (_('Municipality'), {'fields': ('municipality',),'classes':("wide",),'description':_('Select Municipality')}),
        (_('Personal info'), {'fields': ( 'name','contact_number'),'classes':("wide",),'description':_('Enter Your Name')}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':_('Enter Your Address')}),
        (_('Nagrikta Details'), {'fields': ('nagrikta_number', 'jari_jilla','nagrikta_front','nagrikta_back'),'classes':("wide",),'description':_('Enter Your citizenship details')}),
        (_('Anudan Request'),{'fields':('sector','karyakram','samagri','quantity'),'classes':("wide",),'description':_('Select Karyakram and Samagri')}),
        (_('Approval'),{'fields':('approval',),'classes':("wide",),'description':'Test'})

    )


    add_fieldsets = (
        (_('Fiscal Year'),{'fields':('fiscal_year',),'classes':('wide',)}),
        (_('Municipality'), {'fields': ('municipality',),'classes':("wide",),'description':_('Select Municipality')}),
        (_('Personal info'), {'fields': ( 'name','contact_number'),'classes':("wide",),'description':_('Enter Your Name')}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':_('Enter Your Address')}),
        (_('Nagrikta Details'), {'fields': ('nagrikta_number', 'jari_jilla','nagrikta_front','nagrikta_back'),'classes':("wide",),'description':_('Enter Your citizenship details')}),
        (_('Anudan Request'),{'fields':('sector','karyakram','samagri','quantity'),'classes':("wide",),'description':_('Select Karyakram and Samagri')}),

    )

    staff_fieldsets = (
        (_('Municipality'), {'fields': ('municipality',),'classes':("collapse",)}),
        (_('Fiscal Year'),{'fields':('fiscal_year',),'classes':('wide',)}),        
        (_('Personal info'), {'fields': ( 'name','contact_number'),'classes':("wide",),'description':_('Enter Your Name')}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':_('Enter Your Address')}),
        (_('Nagrikta Details'), {'fields': ('nagrikta_number', 'jari_jilla','nagrikta_front','nagrikta_back'),'classes':("wide",),'description':_('Enter Your citizenship details')}),
        (_('Anudan Request'),{'fields':('sector','karyakram','samagri','quantity'),'classes':("wide",),'description':_('Select Karyakram and Samagri')}),

    )

    @admin.action(description='Export to CSV')
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="books.csv"'
        writer = csv.writer(response)
        if '/ne/' in request.path:
            writer.writerow(['नाम','सम्पर्क नम्बर','नगरपालिका','टोल','वडा','कार्यक्रम','सामग्री','मात्रा','स्वीकृति'])
        else:
            writer.writerow(['Name','Contact Number','Municipality','Ward','Tole','Karyakram','Samagri','Quantity','Approval'])
        books = queryset.values_list('name','contact_number','municipality__name','ward__name','tole','karyakram__name', 'samagri__name', 'quantity', 'approval')
        for book in books:
            writer.writerow(book)
        return response

    @admin.action(description='Export to pdf')
    def render_pdf_view(self,request,queryset):
        template_path = 'AnudanPersonal.html'
        context = {'queryset': queryset}
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="AnudanPersonal.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
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
        if not request.user.is_superuser:
            return self.list_filter
        return ['municipality'] + self.list_filter



    

@admin.register(AnudanCompany)
class AnudanCompanyAdmin(admin.ModelAdmin):
    list_display=['firm_name','registration_no','pan_no','vat_no','ward','tole','registered_place','municipality','approval']
    list_display_links=['firm_name','registration_no','pan_no','vat_no']
    list_filter=['fiscal_year','karyakram','ward','approval',]
    actions=[approve,disapprove,'export_to_csv','render_pdf_view']
    form = AnudanCompanyForm
    

    fieldsets = (
        (_('Fiscal Year'),{'fields':('fiscal_year',)}),
        (_('Nagar Palika'), {'fields': ('municipality',),'classes':("wide",),'description':_('Select Municipality')}),
        (_('Firm info'), {'fields': ( 'firm_name','contact_number','pan_no','vat_no','registration_no','registered_place','firm_registration_proof','anya_darta'),'classes':("wide",),'description':_('About Firm')}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':_('Enter Your Address')}),
        (_('Anudan Request'),{'fields':('sector','karyakram','ward_sifaris','prastavan'),'classes':("wide",),'description':_('Select Karyakram')}),
        (_('Approval'),{'fields':('approval',),'classes':("wide",),'description':'Test'})
    )


    add_fieldsets = (
        (_('Fiscal Year'),{'fields':('fiscal_year',)}),
        (_('Nagar Palika'), {'fields': ('municipality'),'classes':("wide",),'description':_('Select Municipality')}),
        (_('Firm info'), {'fields': ( 'firm_name','contact_number','pan_no','vat_no','registration_no','registered_place','firm_registration_proof','anya_darta'),'classes':("wide",),'description':_('About Firm')}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':_('Enter Your Address')}),
        (_('Anudan Request'),{'fields':('sector','karyakram','ward_sifaris','prastavan'),'classes':("wide",),'description':_('Select Karyakram')}),
    )

    staff_fieldsets = (
        (_('Nagar Palika'), {'fields': ('municipality',),'classes':("collapse",),'description':_('Select Municipality')}),
        (_('Fiscal Year'),{'fields':('fiscal_year',)}),
        (_('Firm info'), {'fields': ( 'firm_name','contact_number','pan_no','vat_no','registration_no','registered_place','firm_registration_proof','anya_darta'),'classes':("wide",),'description':_('About Firm')}),
        (_('Address'), {'fields': ('ward', 'tole',),'classes':("wide",),'description':_('Enter Your Address')}),
        (_('Anudan Request'),{'fields':('sector','karyakram','ward_sifaris','prastavan'),'classes':("wide",),'description':_('Select Karyakram')}),
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
            return self.list_filter
        return ['municipality'] + self.list_filter

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
        if '/ne/' in request.path:
            writer.writerow(['नाम','नगरपालिका','टोल','वडा','कार्यक्रम','वडा सिफरिस','प्रस्तावना','स्वीकृति'])
        else:
            writer.writerow(['Name','Municipality','Ward','Tole','Karyakram','Ward Sifaris','Prastavan','Approval'])
        books = queryset.values_list('firm_name','municipality__name','ward__name','tole','karyakram__name','ward_sifaris', 'prastavan','approval')
        for book in books:
            writer.writerow(book)
        return response

    @admin.action(description='Export to pdf')
    def render_pdf_view(self,request,queryset):
        template_path = 'AnudanCompany.html'
        context = {'queryset': queryset}
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="AnudanCompany.pdf"'
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response