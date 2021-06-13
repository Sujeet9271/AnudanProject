from django.db import models
from django.db.models.base import Model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager,AbstractUser,User
from anudaan.models import NagarPalika
# Create your models here.

class CustomAccountManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, password, **other_fields):

        email = self.normalize_email(email)
        user  = self.model(email=email,username=username,first_name=first_name,last_name=last_name, **other_fields)

        user.set_password(password)

        user.save()
        return user


    def create_superuser(self,email,username,first_name,last_name,password,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)

        if other_fields.get('is_staff') is False:
            raise ValueError('Superuser must be assigned is_staff = True')

        if other_fields.get('is_superuser') is False:
            raise ValueError('Superuser must be assigned is_superuser = True')

        return self.create_user(email=email,username=username, password=password, first_name=first_name,last_name=last_name,**other_fields)




class PalikaUser(AbstractBaseUser,PermissionsMixin):
    email        = models.EmailField(_('Email Address'), unique=True)
    username     = models.CharField(max_length=30, unique=True)
    first_name    = models.CharField(max_length=30, blank=True)
    last_name     = models.CharField(max_length=30, blank=True)
    created      = models.DateTimeField(default=timezone.now)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now())
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = CustomAccountManager()

    def __str__(self):
        return f'{self.email}'

    def palika(self):
        return f'{self.Palika}'


class Palika(models.Model):
    user = models.OneToOneField(PalikaUser,on_delete=models.CASCADE,related_name='Palika')
    palika = models.ForeignKey(NagarPalika,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} works in {self.palika.name}'


class Profile(models.Model):
    user = models.OneToOneField(PalikaUser,on_delete=models.CASCADE)
    address = models.CharField(_('Address'),max_length=150,blank=True,null=True)
    contact_number= models.PositiveBigIntegerField(_('Contact Number'),blank=True,null=True)   


    def __str__(self):
        return f"{self.user.username}'s Profile"


