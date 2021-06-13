from django.contrib import admin
from django.http import request
from .models import Karyakram,Samagri,AnudanPerosnal,NagarPalika
from django.utils.translation import gettext_lazy as _
# Register your models here.



@admin.register(NagarPalika)
class NagarPalikaAdmin(admin.ModelAdmin):
    list_display=['id','name']
    list_display_links=['id','name']

class SamagriInline(admin.StackedInline):
    model = Samagri
    extra = 1


@admin.register(Karyakram)
class KaryakramAdmin(admin.ModelAdmin):
    inlines=[SamagriInline]
    list_display=['id','name','nagarpalika']
    list_display_links=['id','name']
    list_filter=['nagarpalika']

    def get_queryset(self, request):
        qs = super(KaryakramAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(nagarpalika=request.user.Palika.palika)


@admin.register(Samagri)
class SamagriAdmin(admin.ModelAdmin):
    list_display=['id','name','karyakram']
    list_filter=['karyakram','nagarpalika']
    list_display_links=['id','name']

    def get_queryset(self, request):
        qs = super(SamagriAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(nagarpalika=request.user.Palika.palika)

@admin.register(AnudanPerosnal)
class AnudanAdmin(admin.ModelAdmin):
    list_display=['id','name','ward','Tole','NagriktaNumber','JariJilla','karyakram','NagriktaFront','NagriktaBack','samagri','approval']
    list_filter=['approval','ward','Tole','JariJilla','karyakram','samagri']
    list_display_links=['id','name']
    list_editable = ['approval']


    fieldsets = (
        
        (_('Nagar Palika'), {'fields': ('nagarpalika',)}),
        (_('Personal info'), {'fields': ( 'name',)}),
        (_('Address'), {'fields': ('ward', 'Tole',)}),
        (_('Nagrikta Details'), {'fields': ('NagriktaNumber', 'JariJilla','NagriktaFront','NagriktaBack')}),
        (_('Anudan Request'),{'fields':('karyakram','samagri')}),
        (_('Approval'),{'fields':('approval')})

    )
    fieldsets = (

        (_('Nagar Palika'), {'fields': ('nagarpalika',)}),
        (_('Personal info'), {'fields': ( 'name',)}),
        (_('Address'), {'fields': ('ward', 'Tole',)}),
        (_('Nagrikta Details'), {'fields': ('NagriktaNumber', 'JariJilla','NagriktaFront','NagriktaBack')}),
        (_('Anudan Request'),{'fields':('karyakram','samagri')}),

    )


    def get_queryset(self, request):
        qs = super(AnudanAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(nagarpalika=request.user.Palika.palika)
