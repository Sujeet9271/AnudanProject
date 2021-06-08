from django.contrib import admin
from .models import PalikaUser,Palika
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class PalikaAdmin(admin.TabularInline):
    model = Palika

class UserAdminConfig(UserAdmin):

    model = PalikaUser
    inlines = [PalikaAdmin]
    ordering = ('-created',)
    search_fields = ('email','username','first_name','last_name',)
    list_filter = ('email','first_name','last_name','created','is_staff','is_superuser','is_active',)
    list_display = ('email','username','first_name','last_name','created','is_staff','is_superuser','is_active','palika')

    fieldsets = (
        (None,{'fields':('email','username')}),
        ('Personal Info',{'fields':('first_name','last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        
    )

    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields':('email','username','first_name','last_name','password1','password2','groups','is_active','is_staff',)
        }),
    )


admin.site.register(PalikaUser,UserAdminConfig)

