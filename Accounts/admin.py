from Municipality.models import Municipality
from django.contrib import admin
from .models import FiscalYear, PalikaUser, MunicipalityStaff, Profile
from django.contrib.auth.admin import UserAdmin,GroupAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm, FiscalYearForm, PalikaStaffForm, ProfileForm
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group

# Unregister models here
admin.site.unregister(Group)


# Register models here

@admin.register(Group)
class CustomGroupAdmin(GroupAdmin):

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'permissions':
                qs = kwargs.get('queryset', db_field.remote_field.model.objects)
                qs = qs.exclude(codename__in=(
                    'add_municipality',
                    'delete_municipality',

                    'add_group',
                    'change_group',
                    'delete_group',
                    'view_group',

                    'add_fiscalyear',
                    'delete_fiscalyear',
                    'change_fiscalyear',

                    'add_permission',
                    'change_permission',
                    'delete_permission',
                    'view_permission',

                    'add_contenttype',
                    'view_contenttype',
                    'change_contenttype',
                    'delete_contenttype',

                    'add_session',
                    'view_session',
                    'delete_session',
                    'change_session',

                    'add_logentry',
                    'view_logentry',
                    'change_logentry',
                    'delete_logentry',
                ))
                
                kwargs['queryset'] = qs.select_related('content_type')
        return super(CustomGroupAdmin, self).formfield_for_manytomany(
                        db_field, request=request, **kwargs)


   
@admin.register(FiscalYear)
class FiscalYearAdmin(admin.ModelAdmin):
    list_display = ['start_date','end_date']
    form = FiscalYearForm


class PalikaStaffAdminInline(admin.TabularInline):
    model = MunicipalityStaff

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'municipality':
            kwargs['queryset'] = Municipality.objects.filter(id = request.user.municipality_staff.municipality.id) if not request.user.is_superuser else Municipality.objects.all()
            kwargs['initial'] = Municipality.objects.filter(id = request.user.municipality_staff.municipality.id) if not request.user.is_superuser else None
        return super(PalikaStaffAdminInline, self).formfield_for_foreignkey(db_field, request, **kwargs)




class ProfileInline(admin.TabularInline):
    model = Profile
  
    
    

@admin.register(PalikaUser)
class UserAdminConfig(UserAdmin):
    model = PalikaUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    inlines = [PalikaStaffAdminInline,ProfileInline]
    list_display = ['id','email', 'username', 'first_name', 'last_name', 'address', 'contact_number', 'is_staff', 'is_admin',
                    'is_superuser', 'municipality_staff',]
    list_display_links = ['email', 'username']
    readonly_fields = ['last_login', 'date_joined']
    list_filter=['is_staff','is_admin']

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
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2',)}),
        (_('Permissions'),{'fields':('is_staff','is_admin','groups','user_permissions')}),
    )


    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'user_permissions':
                qs = kwargs.get('queryset', db_field.remote_field.model.objects)
                qs = qs.exclude(codename__in=(
                    'add_municipality',
                    'delete_municipality',

                    'add_fiscalyear',
                    'delete_fiscalyear',
                    'change_fiscalyear',

                    'add_permission',
                    'change_permission',
                    'delete_permission',

                    'add_contenttype',
                    'view_contenttype',
                    'change_contenttype',
                    'delete_contenttype',

                    'add_session',
                    'view_session',
                    'delete_session',
                    'change_session',

                    'add_logentry',
                    'view_logentry',
                    'change_logentry',
                    'delete_logentry',
                ))
                kwargs['queryset'] = qs.select_related('content_type')
        return super(UserAdminConfig, self).formfield_for_manytomany(
            db_field, request=request, **kwargs)

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
            elif request.user.is_admin:
                    return self.readonly_fields + ['email','is_admin']
            return self.readonly_fields +['email','is_staff', 'is_admin','is_active','groups','user_permissions'] if obj.email==request.user.email else self.readonly_fields+['email','password','username','first_name','last_name','groups','user_permissions','is_staff','is_admin','Profile']
        else:
            if request.user.is_superuser:
                return self.readonly_fields
            elif request.user.is_admin:
                    return self.readonly_fields + ['is_admin']
            return self.readonly_fields +['is_staff', 'is_admin','is_active','groups','user_permissions']

    def has_add_permission(self, request):
        if not request.user.is_admin:
            return False
        return super().has_add_permission(request)

    


# @admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user','address', 'contact_number']


    fieldsets = (
       (_('User Profile'), {'fields': ('user','address','contact_number')}),
    )
   
    def get_queryset(self, request):
        qs = super(ProfileAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = PalikaUser.objects.filter(id = request.user.id) if not request.user.is_superuser else PalikaUser.objects.all()
            kwargs['initial'] = PalikaUser.objects.get(id = request.user.id) if not request.user.is_superuser else None
        return super(ProfileAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)



        
 