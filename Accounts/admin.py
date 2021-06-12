from django.contrib import admin
from .models import PalikaUser,Palika, Profile
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class PalikaAdmin(admin.TabularInline):
    model = Palika


class ProfileInline(admin.TabularInline):
    model = Profile

class UserAdminConfig(UserAdmin):
    model = PalikaUser
    inlines = [PalikaAdmin,ProfileInline]
    

admin.site.register(PalikaUser,UserAdminConfig)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user','address', 'contact_number']
    fields=['address','contact_number']

    def get_queryset(self, request):
        qs = super(ProfileAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    

