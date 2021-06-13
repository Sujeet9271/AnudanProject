from django.contrib import admin
from .models import PalikaUser,Palika, Profile
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm,CustomUserChangeForm
from django.utils.translation import gettext_lazy as _

# Register your models here.




class PalikaAdmin(admin.TabularInline):
    model = Palika


class ProfileInline(admin.TabularInline):
    model = Profile


@admin.register(PalikaUser)
class UserAdminConfig(UserAdmin):
    model = PalikaUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    inlines = [PalikaAdmin,ProfileInline]
    list_display = ['email','username','is_staff','is_superuser','Palika',]
    list_display_links = ['email','username']
    readonly_fields = ['last_login','date_joined']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ( 'username','first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (_('Authentication'), {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ( 'username','first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ( 'is_staff', 'groups', 'user_permissions'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)

    def get_readonly_fields(self, request,obj):
        if obj: # editing an existing object
            return self.readonly_fields +['is_staff', 'is_superuser','is_active','groups','user_permissions','Palika'] if not request.user.is_superuser else self.readonly_fields
        return self.readonly_fields

    
    


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user','address', 'contact_number']
    fields = ['address','contact_number']


    def get_queryset(self, request):
        qs = super(ProfileAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user.id)
    
    def get_fieldsets(self, request,obj):
        return super().get_fieldsets(request, obj=obj)
    

@admin.register(Palika)
class PalikaAdmin(admin.ModelAdmin):
    list_display=['id','user','palika']
    list_display_links=['id','user']
    list_editable = ['palika']

    list_filter = ['palika']
