from django.db import models
from smart_selects.db_fields import ChainedForeignKey

class NagarPalika(models.Model):
    name            = models.CharField(max_length=150)
    contact_number  = models.CharField(max_length=10,default=0)

    def __str__(self):
        return f'{self.name}'


class Karyakram(models.Model):
    nagarpalika     = models.ForeignKey(NagarPalika, on_delete=models.PROTECT)
    name            = models.CharField(max_length=255)
    created         = models.DateTimeField(auto_now_add=True)
    update          = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}-{self.nagarpalika.name}'


class Samagri(models.Model):
    nagarpalika     = models.ForeignKey(NagarPalika, on_delete=models.PROTECT, help_text='Select Nagar Palika')
    karyakram       = ChainedForeignKey(Karyakram,
                                        chained_field="nagarpalika",
                                        chained_model_field="nagarpalika",
                                        on_delete=models.PROTECT,
                                            auto_choose=True)

    name            = models.CharField(max_length=255, help_text='Enter Samagri to Add')

    def __str__(self):
        return f'{self.name}'

    def karyakram_name(self):
        return self.karyakram.name

    class Meta:
        ordering = ['karyakram']

# Storing file for personal Anudan
def personal_location(instance, filename):
    return f"Peronal/{instance.name}/{filename}"

#  Storing file for Company Anudan
def company_location(instance, filename):
    return f"Company{instance.firm_name}/{filename}"


class AnudanPersonal(models.Model):
    nagarpalika         = models.ForeignKey(NagarPalika, on_delete=models.PROTECT)
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
                                               chained_field="nagarpalika",
                                               chained_model_field="nagarpalika",
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


class AnudanCompany(models.Model):
    nagarpalika             = models.ForeignKey(NagarPalika, on_delete=models.PROTECT)
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