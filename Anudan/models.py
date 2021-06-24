from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from django.utils.translation import gettext_lazy as _

class Municipality(models.Model):
    name            = models.CharField(verbose_name=_('name'),max_length=150)
    contact_number  = models.CharField(verbose_name=_('contact number'),max_length=10,default=0)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table='Municipality'
        verbose_name = _('Municipality')
        verbose_name_plural = _('Municipalities')


class Karyakram(models.Model):
    municipality     = models.ForeignKey(Municipality,on_delete=models.PROTECT,verbose_name=_('Municipality'))
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
    name                = models.CharField(max_length=255,verbose_name=_('name'))
    ward                = models.PositiveIntegerField(max_length=2,verbose_name=_('ward'))
    tole                = models.CharField(max_length=255,verbose_name=_('tole'))
    nagrikta_number     = models.PositiveBigIntegerField(max_length=12, verbose_name=_('Nagrikta Number'))
    jari_jilla          = models.CharField(max_length=20, verbose_name=_('Jaari Jilla'))
    karyakram           = ChainedForeignKey(Karyakram,
                                               chained_field="municipality",
                                               chained_model_field="municipality",
                                               on_delete=models.PROTECT,
                                                   auto_choose=True,
                                                   verbose_name=_('Karyakram'))        
    nagrikta_front      = models.ImageField(upload_to=personal_location, verbose_name=_('Nagrikta Front Photo'))
    nagrikta_back       = models.ImageField(upload_to=personal_location, verbose_name=_('Nagrikta Back Photo'),blank = True)
    samagri             = ChainedForeignKey(Samagri,
                                               chained_field="karyakram",
                                               chained_model_field="karyakram",
                                               auto_choose=True,
                                               on_delete=models.PROTECT,
                                               verbose_name=_('Samagri')
                                               )
    quantity            = models.PositiveSmallIntegerField(default=1)
    approval            = models.CharField(choices=choices_approval, default='Not Approved', max_length=14,verbose_name=_('approval'))

    
    
    def __str__(self):
        return f'{self.name}-{self.karyakram}-{self.samagri}-{self.approval}'

    class Meta:
        db_table='Anudan_Personal'
        verbose_name = _('Anudan Personal')
        verbose_name_plural = _('Anudan Personal')



class AnudanCompany(models.Model):
    fiscal_year         = models.ForeignKey(to='Accounts.FiscalYear',verbose_name=_('Fiscal Year'),on_delete = models.DO_NOTHING,default=1)
    municipality             = models.ForeignKey(Municipality, on_delete=models.PROTECT)
    choices_approval        = (
                                   ('Approved', ('Approved')),
                                   ('Not Approved', ('Not Approved'))
                               )
    firm_name               = models.CharField(max_length=255)
    pan_no                  = models.PositiveIntegerField(max_length=2)
    vat_no                  = models.CharField(max_length=255)
    registration_no         = models.PositiveBigIntegerField(max_length=12, verbose_name='Registration Number')
    ward                    = models.PositiveIntegerField(max_length=2)
    tole                    = models.CharField(max_length=255)    
    registered_place        = models.CharField(max_length=20, verbose_name='Jaari Jilla')
    choices_darta                 = (
                                    ('Gharelu',('Gharelu')),
                                    ('Vanijya',('Vanijya'))
                                )
    anya_darta              = models.CharField(choices=choices_darta,max_length=50,blank=True,null=True)
    firm_registration_proof = models.ImageField(upload_to=company_location, verbose_name='Firm Registration Proof')
    ward_sifaris            = models.ImageField(upload_to=company_location, verbose_name='Ward Sifaris')
    prastavan               = models.ImageField(upload_to=company_location, verbose_name='Upload Prastavan')

    approval                = models.CharField(choices=choices_approval, default='Not Approved', max_length=14)

    def __str__(self):
        return f'{self.firm_name}-{self.registration_no}-{self.approval}'

    class Meta:
        db_table='Anudan_Company'
        verbose_name = _('Anudan Company')
        verbose_name_plural = _('Anudan Company')

