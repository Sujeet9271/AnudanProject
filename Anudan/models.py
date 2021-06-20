from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from django.utils.translation import ugettext_lazy as _

class Municipality(models.Model):
    name            = models.CharField(_('name'),max_length=150)
    contact_number  = models.CharField(_('phonenumber'),max_length=10,default=0)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table='Municipality'
        verbose_name = _('Municipality')
        verbose_name_plural = _('Municipalities')


class Karyakram(models.Model):
    municipality     = models.ForeignKey(Municipality,on_delete=models.PROTECT,help_text=_('Select Municipality'))
    name            = models.CharField(_('name'),max_length=255)
    created         = models.DateTimeField(_('created'),auto_now_add=True)
    update          = models.DateTimeField(_('update'),auto_now=True)

    def __str__(self):
        return f'{self.name}-{self.municipality.name}'
    
    class Meta:
        db_table='Karyakram'
        verbose_name= _('Karyakram')
        verbose_name_plural = _('Karyakram')


class Samagri(models.Model):
    municipality     = models.ForeignKey(Municipality, on_delete=models.PROTECT, help_text=_('Select Municipality'))
    karyakram       = ChainedForeignKey(Karyakram,
                                        chained_field="municipality",
                                        chained_model_field="municipality",
                                        on_delete=models.PROTECT,
                                        auto_choose=True)

    name            = models.CharField(_('name'),max_length=255, help_text='Enter Samagri to Add')

    def __str__(self):
        return f'{self.name}'

    def karyakram_name(self):
        return self.karyakram.name

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
    municipality         = models.ForeignKey(Municipality, on_delete=models.PROTECT,help_text=_('Select Municipality'))
    choices_approval    = (
                               ('Approved', ('Approved')),
                               ('Not Approved', ('Not Approved'))
                           )
    name                = models.CharField(max_length=255)
    ward                = models.PositiveIntegerField(max_length=2)
    tole                = models.CharField(max_length=255)
    nagrikta_number     = models.PositiveBigIntegerField(max_length=12, verbose_name='Nagrikta Number')
    jari_jilla          = models.CharField(max_length=20, verbose_name='Jaari Jilla')
    karyakram           = ChainedForeignKey(Karyakram,
                                               chained_field="municipality",
                                               chained_model_field="municipality",
                                               on_delete=models.PROTECT,
                                                   auto_choose=True)        
    nagrikta_front      = models.ImageField(upload_to=personal_location, verbose_name='Nagrikta Front Photo')
    nagrikta_back       = models.ImageField(upload_to=personal_location, verbose_name='Nagrikta Back Photo')
    samagri             = ChainedForeignKey(Samagri,
                                               chained_field="karyakram",
                                               chained_model_field="karyakram",
                                               auto_choose=True,
                                               on_delete=models.PROTECT
                                               )
    approval            = models.CharField(choices=choices_approval, default='Not Approved', max_length=14)

    
    
    def __str__(self):
        return f'{self.name}-{self.karyakram}-{self.samagri}-{self.approval}'

    class Meta:
        db_table='Anudan_Personal'
        verbose_name = _('Anudan Personal')
        verbose_name_plural = _('Anudan Personal')

class AnudanCompany(models.Model):
    municipality             = models.ForeignKey(Municipality, on_delete=models.PROTECT,help_text=_('Select Municipality'))
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