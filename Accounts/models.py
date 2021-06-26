from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from Municipality.models import Municipality


# Create your models here.

class CustomAccountManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, password, **other_fields):

        email = self.normalize_email(email)
        user  = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **other_fields)

        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, username, first_name, last_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_admin', True)

        if other_fields.get('is_staff') is False:
            raise ValueError('Superuser must be assigned is_staff = True')

        if other_fields.get('is_superuser') is False:
            raise ValueError('Superuser must be assigned is_superuser = True')

        return self.create_user(email=email, username=username, password=password, first_name=first_name,
                                last_name=last_name, **other_fields)


class PalikaUser(AbstractBaseUser, PermissionsMixin):
    email        = models.EmailField(verbose_name=_('email'), unique=True)
    username     = models.CharField(verbose_name=_('username'),max_length=30, unique=True)
    first_name   = models.CharField(verbose_name=_('first name'),max_length=30, blank=True)
    last_name    = models.CharField(verbose_name=_('last name'),max_length=30, blank=True)
    created      = models.DateTimeField(verbose_name=_('created'),default=timezone.now)
    is_active    = models.BooleanField(verbose_name=_('is active'),default=True)
    is_staff     = models.BooleanField(verbose_name=_('is staff'),default=False)
    is_admin     = models.BooleanField(verbose_name=_('is admin'),default=False)
    is_superuser = models.BooleanField(verbose_name=_('is superuser'),default=False)
    date_joined  = models.DateField(verbose_name=_('date joined'),auto_now_add=True,auto_now=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomAccountManager()

    def __str__(self):
        return f'{self.email}'


    def address(self):
        return f'{self.Profile.address}'
    address.short_description = _('address')

    

    def contact_number(self):
        return f'{self.Profile.contact_number}'
    contact_number.short_description = _('contact number')


    def get_fullname(self):
        if self.first_name=='':
            return self.get_username()
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table='Users'
        verbose_name = _('user')
        verbose_name_plural = _('users')



class MunicipalityStaff(models.Model):
    user        = models.OneToOneField(PalikaUser, on_delete=models.CASCADE, related_name='municipality_staff',verbose_name=_('user'),)
    municipality      = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='municipality_staff',verbose_name=_('Municipality'),)

    def __str__(self):
        return f'{self.user.username} works in {self.municipality.name}'

    class Meta:
        db_table = 'Staff'
        verbose_name = _('staff')
        verbose_name_plural = _('staffs')


class Profile(models.Model):
    user             = models.OneToOneField(PalikaUser,verbose_name=_('user'), on_delete=models.CASCADE,related_name='Profile')
    address          = models.CharField(verbose_name=_('address'), max_length=150, blank=True, null=True)
    contact_number   = models.PositiveBigIntegerField(verbose_name=_('contact number'), blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        db_table='Profile'
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'





class FiscalYear(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.start_date}/{self.end_date}'

    class Meta:
        db_table = 'Fiscal_Year'
        verbose_name = _('Fiscal Year')
        verbose_name_plural = _('Fiscal Year')

