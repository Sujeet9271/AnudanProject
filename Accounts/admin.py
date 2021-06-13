from django.contrib import admin
from .models import PalikaUser,Palika, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import forms
from .forms import CustomUserCreationForm
from django.utils.translation import gettext_lazy as _

# Register your models here.

# class CustomUserCreationForm(forms.UserCreationForm):
#     class Meta:
#         model = PalikaUser
#         fields = ('email','username',)

class CustomUserChangeForm(forms.UserChangeForm):
    class Meta:
        model = PalikaUser
        fields = ('email','username','first_name','last_name',)

class PalikaAdmin(admin.TabularInline):
    model = Palika


class ProfileInline(admin.TabularInline):
    model = Profile

class UserAdminConfig(UserAdmin):
    model = PalikaUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    inlines = [PalikaAdmin,ProfileInline]
    list_display = ['email','username','is_staff','is_superuser','Palika',]
    list_display_links = ['email','username']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ( 'username','first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','username','first_name','last_name', 'password1', 'password2','is_staff','groups'),
        }),
    )
    

admin.site.register(PalikaUser,UserAdminConfig)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user','address', 'contact_number']
    fields=['user','address','contact_number']

    def get_queryset(self, request):
        qs = super(ProfileAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)
    
    
    
    def get_fieldsets(self, request,obj):
        return super().get_fieldsets(request, obj=obj)
    

