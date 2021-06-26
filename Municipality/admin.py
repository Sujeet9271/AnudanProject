from Accounts.models import FiscalYear
from Municipality.models import Municipality, Sector, Ward
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Register your models here.
@admin.register(Municipality)
class NagarPalikaAdmin(admin.ModelAdmin):
    list_display=['id','name','contact_number']
    list_display_links=['id','name',]


    def has_add_permission(self, request):
        if not request.user.is_admin:
            return False
        return super().has_add_permission(request)


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display=['id','name','municipality']

    def get_queryset(self, request):
        return super(SectorAdmin,self).get_queryset(request) if request.user.is_superuser else super(SectorAdmin,self).get_queryset(request).filter(municipality = request.user.municipality_staff.municipality.id)


    def has_add_permission(self, request):
        if not request.user.is_admin:
            return False
        return super().has_add_permission(request)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'municipality':
            kwargs['queryset'] = Municipality.objects.filter(id = request.user.municipality_staff.municipality.id) if not request.user.is_superuser else Municipality.objects.all()
            kwargs['initial'] = Municipality.objects.get(id = request.user.municipality_staff.municipality.id) if not request.user.is_superuser else None
        
        return super(SectorAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

   
@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display=['id','name','municipality']
    list_filter=['municipality']

    def get_queryset(self, request):
        qs = super(WardAdmin,self).get_queryset(request)
        return qs if request.user.is_superuser else qs.filter(municipality = request.user.municipality_staff.municipality.id)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'municipality':
            kwargs['queryset'] = Municipality.objects.filter(id = request.user.municipality_staff.municipality.id) if not request.user.is_superuser else Municipality.objects.all()
            kwargs['initial'] = Municipality.objects.get(id = request.user.municipality_staff.municipality.id) if not request.user.is_superuser else None
        return super(WardAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    