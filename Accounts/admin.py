from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PalikaUser, PalikaStaff, Profile
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.utils.translation import gettext_lazy as _


# Register your models here.


class PalikaAdmin(admin.TabularInline):
    model = PalikaStaff


class ProfileInline(admin.TabularInline):
    model = Profile


@admin.register(PalikaUser)
class UserAdminConfig(UserAdmin):
    model = PalikaUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    inlines = [PalikaAdmin, ProfileInline]
    list_display = ['email', 'username', 'first_name', 'last_name', 'address', 'contact_number', 'is_staff', 'is_admin',
                    'is_superuser', 'palika_staff', ]
    list_display_links = ['email', 'username']
    readonly_fields = ['last_login', 'date_joined']

    fieldsets = (
        ('User Details', {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_admin', 'groups', 'user_permissions'),
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
            return qs.filter(palika_staff__palika=request.user.palika_staff.palika.id).exclude(id=request.user.id)
        return qs.filter(id=request.user.id)


    def get_readonly_fields(self, request,obj):
        if obj: # editing an existing object
            if request.user.is_superuser:
                return self.readonly_fields
            return self.readonly_fields +['is_staff', 'is_admin','is_active','groups','user_permissions','Palika'] if not request.user.is_admin else self.readonly_fields
        return self.readonly_fields


    # def get_readonly_fields(self, request, obj):
    #     if obj:  # editing an existing object
    #         self.readonly_fields
    #         if request.user.is_superuser:
    #             return self.readonly_fields
    #         if not request.user.is_admin:
    #             self.readonly_fields + ['is_staff', 'is_admin', 'is_active', 'groups','user_permissions'] 
    #         else:
    #             self.readonly_fields + ['is_admin', 'is_active','user_permissions']
    #         return 
    #     return self.readonly_fields

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display=['user','address', 'contact_number']
#     fields = ['address','contact_number','user']


#     def get_queryset(self, request):
#         qs = super(ProfileAdmin, self).get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(user=request.user)

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(user=request.user.id)

#     def get_fieldsets(self, request,obj):
#         return super().get_fieldsets(request, obj=obj)


# @admin.register(PalikaStaff)
# class PalikaStaffAdmin(admin.ModelAdmin):
#     list_display=['id','user','palika']
#     list_display_links=['id','user']
#     list_editable = ['palika']
#     list_filter = ['palika']
