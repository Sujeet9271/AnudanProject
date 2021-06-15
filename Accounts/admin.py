from django.contrib import admin
from .models import PalikaUser, PalikaStaff, Profile
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm, PalikaStaffForm, ProfileForm
from django.utils.translation import gettext_lazy as _
from django.forms.models import BaseInlineFormSet



# Register your models here.





class PalikaStaffAdmin(admin.TabularInline):
    model = PalikaStaff
    




@admin.register(PalikaUser)
class UserAdminConfig(UserAdmin):
    model = PalikaUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    # inlines = [PalikaStaffAdmin]
    list_display = ['email', 'username', 'first_name', 'last_name', 'address', 'contact_number', 'is_staff', 'is_admin',
                    'is_superuser', 'palika_staff', ]
    list_display_links = ['email', 'username']
    readonly_fields = ['last_login', 'date_joined']

    fieldsets = (
        ('User Details', {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_admin', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (_('Staff Registration'), {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2',),
        }),
        (_('Permissions'),{'fields':('is_staff','is_admin','groups',)}),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_admin:
            return qs.filter(palika_staff__palika=request.user.palika_staff.palika.id)
        return qs.filter(id=request.user.id)


    def get_readonly_fields(self, request,obj):
        if obj:
            if request.user.is_superuser:
                return self.readonly_fields
            elif request.user.is_admin:
                return self.readonly_fields + ['is_admin','user_permissions']
            return self.readonly_fields +['is_staff', 'is_admin','is_active','groups','user_permissions','Palika']
        else:
            if request.user.is_superuser:
                return self.readonly_fields
            elif request.user.is_admin:
                    return self.readonly_fields + ['is_admin','user_permissions']
            return self.readonly_fields +['is_staff', 'is_admin','is_active','groups','user_permissions','Palika']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user','address', 'contact_number']
    fields = ['user','address','contact_number']
    form = ProfileForm


    def get_queryset(self, request):
        qs = super(ProfileAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


    def get_form(self, request,*args, **kwargs):
        form = super(ProfileAdmin,self).get_form(request,*args, **kwargs)
        form.current_user=request.user
        return form

@admin.register(PalikaStaff)
class PalikaStaffAdmin(admin.ModelAdmin):
    list_display=['id','user','palika']
    list_display_links=['id','user']
    list_filter = ['palika']
    fields=['user','palika']
    form = PalikaStaffForm


    def get_form(self, request,*args, **kwargs):
        form = super(PalikaStaffAdmin,self).get_form(request,*args, **kwargs)
        form.current_user=request.user
        return form

    def get_queryset(self, request):
        qs = super(PalikaStaffAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(palika=request.user.palika_staff.palika)

    # def get_readonly_fields(self, request, obj):
    #     if obj: 
    #         if request.user.is_superuser:
    #             return self.readonly_fields
    #         elif request.user.is_admin:
    #             return self.readonly_fields + ('user',)
    #         return self.readonly_fields +('user','palika')
    #     else:
    #         if request.user.is_superuser:
    #             return self.readonly_fields
    #         elif request.user.is_admin:
    #             return self.readonly_fields + ('user',)
    #         return self.readonly_fields + ('user','palika')
        
    

