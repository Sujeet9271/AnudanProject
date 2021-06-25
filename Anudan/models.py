from functools import WRAPPER_UPDATES

from django.db.models.base import ModelState
from Accounts.models import FiscalYear
from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from django.utils.translation import gettext_lazy as _
from Municipality.models import Municipality, Sector



class Karyakram(models.Model):
    municipality     = models.ForeignKey(Municipality,on_delete=models.PROTECT,verbose_name=_('Municipality'))
    sector           = ChainedForeignKey(Sector,chained_field="municipality",
                                        chained_model_field="municipality",
                                        on_delete=models.PROTECT,
                                        auto_choose=True,
                                        verbose_name=_('Sector'),default=1)

    name            = models.CharField(verbose_name=_('name'),max_length=255)
    created         = models.DateTimeField(verbose_name=_('created'),auto_now_add=True)

    def __str__(self):
        return f'{self.name}-{self.municipality.name}'
    
    class Meta:
        db_table='Karyakram'
        verbose_name= _('Karyakram')
        verbose_name_plural = _('Karyakram')


class Unit(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.name}'


class Samagri(models.Model):
    karyakram       = ChainedForeignKey(Karyakram,
                                        chained_field="municipality",
                                        chained_model_field="municipality",
                                        on_delete=models.PROTECT,
                                        auto_choose=True,
                                        verbose_name=_('Karyakram')
                                        )

    name            = models.CharField(verbose_name=_('name'),max_length=255,)
    quantity        = models.IntegerField(default=1)
    unit            = models.ForeignKey(Unit,verbose_name=_('Units'),on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.name}'

    def karyakram_name(self):
        return self.karyakram.name
    karyakram_name.short_description = _('Karyakram name')


    class Meta:
        db_table='Samagri'
        ordering = ['karyakram']
        verbose_name = _('Samagri')
        verbose_name_plural = _('Samagri')

# Storing file for personal Anudan
def personal_location(instance, filename):
    return f"Personal/{instance.name}/{filename}"

#  Storing file for Company Anudan
def company_location(instance, filename):
    return f"Company/{instance.firm_name}/{filename}"


class AnudanPersonal(models.Model):
    fiscal_year         = models.ForeignKey(to='Accounts.FiscalYear',verbose_name=_('Fiscal Year'),on_delete = models.DO_NOTHING,)
    municipality        = models.ForeignKey(Municipality, on_delete=models.PROTECT,verbose_name=_('Municipality'))
    choices_approval    = (
                               ('Approved', ('Approved')),
                               ('Not Approved', ('Not Approved'))
                           )
    name                = models.CharField(max_length=255,verbose_name=_('Name'))
    ward                = models.PositiveIntegerField(verbose_name=_('Ward'))
    tole                = models.CharField(max_length=255,verbose_name=_('Tole'))
    nagrikta_number     = models.PositiveBigIntegerField(verbose_name=_('Nagrikta Number'))
    nagrikta_front      = models.ImageField(upload_to=personal_location, verbose_name=_('Nagrikta Front Photo'))
    nagrikta_back       = models.ImageField(upload_to=personal_location, verbose_name=_('Nagrikta Back Photo'),blank = True)
    jari_jilla          = models.CharField(max_length=20, verbose_name=_('Jaari Jilla'))


    sector           = ChainedForeignKey(Sector,chained_field="municipality",
                                        chained_model_field="municipality",
                                        on_delete=models.PROTECT,
                                        auto_choose=True,
                                        verbose_name=_('Sector'),default=1)

    karyakram           = ChainedForeignKey(Karyakram,
                                               chained_field="sector",
                                               chained_model_field="sector",
                                               on_delete=models.PROTECT,
                                                   auto_choose=True,
                                                   verbose_name=_('Karyakram'))        
    
    samagri             = ChainedForeignKey(Samagri,
                                               chained_field="karyakram",
                                               chained_model_field="karyakram",
                                               auto_choose=True,
                                               on_delete=models.PROTECT,
                                               verbose_name=_('Samagri')
                                               )
    quantity            = models.PositiveSmallIntegerField(default=1)
    approval            = models.CharField(choices=choices_approval, default='Not Approved', max_length=14,verbose_name=_('Approval'))

    
    
    def __str__(self):
        return f'{self.name}-{self.karyakram}-{self.samagri}-{self.approval}'

    class Meta:
        db_table='Anudan_Personal'
        verbose_name = _('Anudan Personal')
        verbose_name_plural = _('Anudan Personal')



class AnudanCompany(models.Model):
    fiscal_year             = models.ForeignKey(to='Accounts.FiscalYear',verbose_name=_('Fiscal Year'),on_delete = models.DO_NOTHING,default=1)
    municipality            = models.ForeignKey(Municipality, on_delete=models.PROTECT,verbose_name=_('Municipality'))
    choices_approval        = (
                                   ('Approved', ('Approved')),
                                   ('Not Approved', ('Not Approved'))
                               )
    firm_name               = models.CharField(max_length=255,verbose_name=_('Firm name'))
    pan_no                  = models.PositiveBigIntegerField(verbose_name=_('PAN no'),)
    vat_no                  = models.PositiveBigIntegerField(verbose_name=_('VAT no'))
    registration_no         = models.PositiveBigIntegerField(verbose_name=_('Registration Number'))
    ward                    = models.PositiveSmallIntegerField(verbose_name=_('Ward'))
    tole                    = models.CharField(max_length=255,verbose_name=_('Tole'))    
    registered_place        = models.CharField(max_length=20, verbose_name=_('Jaari Jilla'))
    choices_darta                 = (
                                    ('Gharelu',('Gharelu')),
                                    ('Banijya',('Banijya'))
                                )
    anya_darta              = models.CharField(choices=choices_darta,max_length=50,blank=True,null=True,verbose_name=_('Registered as'))
    firm_registration_proof = models.ImageField(upload_to=company_location, verbose_name=_('Firm Registration Proof'))
    ward_sifaris            = models.ImageField(upload_to=company_location, verbose_name=_('Ward Sifaris'))
    prastavan               = models.ImageField(upload_to=company_location, verbose_name=_('Upload Prastavan'))

    approval                = models.CharField(choices=choices_approval, default='Not Approved', max_length=14,verbose_name=_('Approval'))

    def __str__(self):
        return f'{self.firm_name}-{self.registration_no}-{self.approval}'

    class Meta:
        db_table='Anudan_Company'
        verbose_name = _('Anudan Company')
        verbose_name_plural = _('Anudan Company')

# class AnudanCompany(models.Model):
#     municipality             = models.ForeignKey(Municipality, on_delete=models.PROTECT)
#     fiscal_year  = models.ForeignKey(FiscalYear,on_delete=models.DO_NOTHING)
#     choices_approval        = (
#                                    ('Approved', ('Approved')),
#                                    ('Not Approved', ('Not Approved'))
#                                )
#     firm_name               = models.CharField(max_length=255)
#     pan_no                  = models.PositiveIntegerField(max_length=2)
#     vat_no                  = models.CharField(max_length=255)
#     registration_no         = models.PositiveBigIntegerField(max_length=12, verbose_name='Registration Number')
#     ward                    = models.PositiveIntegerField(max_length=2)
#     tole                    = models.CharField(max_length=255)    
#     registered_place        = models.CharField(max_length=20, verbose_name='Jaari Jilla')
#     firm_registration_proof = models.ImageField(upload_to=company_location, verbose_name='Firm Registration Proof')
#     choices_darta           = (
#                                     ('Gharelu',('Gharelu')),
#                                     ('Banijya',('Banijya'))
#                                 )
#     anya_darta              = models.CharField(choices=choices_darta,max_length=50,blank=True,null=True,verbose_name=_('Registered as'))
#     ward_sifaris            = models.ImageField(upload_to=company_location, verbose_name='Ward Sifaris')
#     prastavan               = models.ImageField(upload_to=company_location, verbose_name='Upload Prastavan')
#     approval                = models.CharField(choices=choices_approval, default='Not Approved', max_length=14)

#     def __str__(self):
#         return f'{self.firm_name}-{self.registration_no}-{self.approval}'

#     class Meta:
#         db_table = 'Anudan_Company'
#         verbose_name_plural = 'Anudan Company'


class MedicineRequest(models.Model):
    municipality    =   models.ForeignKey(Municipality,on_delete=models.DO_NOTHING,verbose_name=_('Municipality'))
    name    = models.CharField(verbose_name=_('Name'),max_length=150)
    ward    = models.PositiveSmallIntegerField(verbose_name=_('Ward'))
    tole    = models.CharField(verbose_name=_('Tole'),max_length=150)
    medicine    = models.CharField(verbose_name=_('Medicine'),max_length=150)
    quantity    = models.PositiveSmallIntegerField(_('Quantity'))  


    def __str__(self):
        return f'{self.ward}-{self.tole}-{self.name}-{self.medicine}-{self.quantity}'