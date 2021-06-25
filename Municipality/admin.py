from Municipality.models import Municipality, Sector
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

    # def has_delete_permission(self, request, obj):
    #     if not request.user.is_admin:
    #         return False
    #     return super().has_delete_permission(request, obj=obj)

    # def has_change_permission(self, request, obj):
    #     if not request.user.is_admin:
    #         return False
    #     return super().has_change_permission(request, obj=obj)

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display=['id','name','municipality']

    def get_queryset(self, request):
        return super(SectorAdmin,self).get_queryset(request) if request.user.is_superuser else super(SectorAdmin,self).get_queryset(request).filter(municipality = request.user.municipality_staff.municipality.id)


    def has_add_permission(self, request):
        if not request.user.is_admin:
            return False
        return super().has_add_permission(request)

    # def has_delete_permission(self, request, obj):
    #     if not request.user.is_admin:
    #         return False
    #     return super().has_delete_permission(request, obj=obj)

    # def has_change_permission(self, request, obj):
    #     if not request.user.is_admin:
    #         return False
    #     return super().has_change_permission(request, obj=obj)