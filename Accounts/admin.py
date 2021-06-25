from Municipality.models import Municipality
from django.contrib import admin
from .models import FiscalYear, PalikaUser, MunicipalityStaff, Profile
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm, PalikaStaffForm, ProfileForm
from django.utils.translation import gettext as _



# Register your models here.
   
@admin.register(FiscalYear)
class FiscalYearAdmin(admin.ModelAdmin):
    list_display = ['start_date','end_date']


class PalikaStaffAdminInline(admin.TabularInline):
    model = MunicipalityStaff

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'municipality':
            kwargs['queryset'] = Municipality.objects.filter(id = request.user.municipality_staff.municipality.id) if not request.user.is_superuser else Municipality.objects.all()
            kwargs['initial'] = Municipality.objects.get(id = request.user.municipality_staff.municipality.id) if not request.user.is_superuser else None
        return super(PalikaStaffAdminInline, self).formfield_for_foreignkey(db_field, request, **kwargs)


class ProfileInline(admin.TabularInline):
    model = Profile
    

@admin.register(PalikaUser)
class UserAdminConfig(UserAdmin):
    model = PalikaUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    inlines = [PalikaStaffAdminInline,ProfileInline]
    list_display = ['email', 'username', 'first_name', 'last_name', 'address', 'contact_number', 'is_staff', 'is_admin',
                    'is_superuser', 'municipality_staff', ]
    list_display_links = ['email', 'username']
    readonly_fields = ['last_login', 'date_joined']

    fieldsets = (
        (_('User Details'), {'fields': ('email', 'password')}),
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
            return qs.filter(municipality_staff__municipality=request.user.municipality_staff.municipality.id)
        return qs.filter(id=request.user.id)


    def get_readonly_fields(self, request,obj):
        if obj:
            if request.user.is_superuser:
                return self.readonly_fields
            elif not request.user.is_superuser:
                if obj.is_admin:
                    return self.readonly_fields+['is_admin','groups','user_permissions']
                else:
                    if obj.email != request.user.email:
                        return self.readonly_fields + ['email','username','first_name','last_name','is_staff','is_admin','groups','permissions']                    
                return self.readonly_fields + ['is_admin','user_permissions']
            return self.readonly_fields +['is_staff', 'is_admin','is_active','groups','user_permissions','Palika']
        else:
            if request.user.is_superuser:
                return self.readonly_fields
            elif request.user.is_admin:
                    return self.readonly_fields + ['is_admin','user_permissions']
            return self.readonly_fields +['is_staff', 'is_admin','is_active','groups','user_permissions','Palika']

    def has_add_permission(self, request):
        if not request.user.is_admin:
            return False
        return super().has_add_permission(request)

    


# @admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user','address', 'contact_number']
    form = ProfileForm


    fieldsets = (
       (_('User Profile'), {'fields': ('user','address','contact_number')}),
    )
   
    def get_queryset(self, request):
        qs = super(ProfileAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


    def get_form(self, request,*args, **kwargs):
        form = super(ProfileAdmin,self).get_form(request,*args, **kwargs)
        form.current_user=request.user
        return form

    # def get_fieldsets(self, request, obj):
    #     if obj:
    #         return self.fieldsets
    #     return self.add_fieldsets



# @admin.register(MunicipalityStaff)
class PalikaStaffAdmin(admin.ModelAdmin):
    list_display=['id','user','municipality']
    list_display_links=['id','user']
    list_filter = ['municipality']
    fields=['user','municipality']
    form = PalikaStaffForm


    def get_form(self, request,*args, **kwargs):
        form = super(PalikaStaffAdmin,self).get_form(request,*args, **kwargs)
        form.current_user=request.user
        return form

    def get_queryset(self, request):
        qs = super(PalikaStaffAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(municipality=request.user.municipality_staff.municipality)

        
 