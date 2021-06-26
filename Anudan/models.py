from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from django.utils.translation import gettext_lazy as _
from Municipality.models import Municipality, Sector, Ward



class Karyakram(models.Model):
    municipality     = models.ForeignKey(Municipality,on_delete=models.PROTECT,verbose_name=_('Municipality'))
    sector           = ChainedForeignKey(Sector,chained_field="municipality",
                                        chained_model_field="municipality",
                                        on_delete=models.PROTECT,
                                        auto_choose=True,
                                        verbose_name=_('Sector'))

    name            = models.CharField(verbose_name=_('Name'),max_length=255)
    created         = models.DateTimeField(verbose_name=_('created'),auto_now_add=True)

    def __str__(self):
        return f'{self.name}-{self.municipality.name}'
    
    class Meta:
        db_table='Karyakram'
        verbose_name= _('Karyakram')
        verbose_name_plural = _('Karyakram')


class Unit(models.Model):
    name = models.CharField(max_length=50,verbose_name=_('Name'))
    
    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table='Unit'
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')


class Samagri(models.Model):
    karyakram       = ChainedForeignKey(Karyakram,
                                        chained_field="municipality",
                                        chained_model_field="municipality",
                                        on_delete=models.PROTECT,
                                        auto_choose=True,
                                        verbose_name=_('Karyakram')
                                        )

    name            = models.CharField(verbose_name=_('Name'),max_length=255,)
    quantity        = models.IntegerField(default=1,verbose_name=_('Quantity'))
    unit            = models.ForeignKey(Unit,verbose_name=_('Units'),null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.name}'

    def karyakram_name(self):
        return self.karyakram.name
    karyakram_name.short_description = _('Karyakram')


    class Meta:
        db_table='Samagri'
        ordering = ['karyakram']
        verbose_name = _('Samagri')
        verbose_name_plural = _('Samagri')

# Storing file for personal Anudan
def personal_location(instance, filename):
    return f"{instance.municipality.name}/Personal/{instance.name}/{filename}"

#  Storing file for Company Anudan
def company_location(instance, filename):
    return f"{instance.municipality.name}/Company/{instance.firm_name}/{filename}"


class AnudanPersonal(models.Model):
    fiscal_year         = models.ForeignKey(to='Accounts.FiscalYear',verbose_name=_('Fiscal Year'),on_delete = models.PROTECT,)
    municipality        = models.ForeignKey(Municipality, on_delete=models.PROTECT,verbose_name=_('Municipality'))
    choices_approval    = (
                               ('Approved', _('Approved')),
                               ('Not Approved', _('Not Approved'))
                           )
    name                = models.CharField(max_length=255,verbose_name=_('Name'))
    
    ward                = ChainedForeignKey(Ward,chained_field="municipality",
                                        chained_model_field="municipality",
                                        on_delete=models.PROTECT,
                                        auto_choose=True,
                                        verbose_name=_('Ward'))  
    tole                = models.CharField(verbose_name=_('Tole'),max_length=150)
    nagrikta_number     = models.CharField(verbose_name=_('Nagrikta Number'),max_length=20)
    nagrikta_front      = models.ImageField(upload_to=personal_location, verbose_name=_('Nagrikta Front Photo'))
    nagrikta_back       = models.ImageField(upload_to=personal_location, verbose_name=_('Nagrikta Back Photo'),blank = True)
    jari_jilla          = models.CharField(max_length=20, verbose_name=_('Jaari Jilla'))

    contact_number = models.CharField(verbose_name=_('Contact Number'),max_length=20)


    sector           = ChainedForeignKey(Sector,chained_field="municipality",
                                        chained_model_field="municipality",
                                        on_delete=models.PROTECT,
                                        auto_choose=True,
                                        verbose_name=_('Sector'))

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
    created             = models.DateField(verbose_name=_('created'),auto_now_add=True,auto_now=False)
    updated             = models.DateField(verbose_name=_('updated'),auto_now=True)


    
    
    def __str__(self):
        return f'{self.name}-{self.karyakram}-{self.samagri}-{self.approval}'

    class Meta:
        db_table='Anudan_Personal'
        verbose_name = _('Anudan Personal')
        verbose_name_plural = _('Anudan Personal')



class AnudanCompany(models.Model):
    fiscal_year             = models.ForeignKey(to='Accounts.FiscalYear',verbose_name=_('Fiscal Year'),on_delete = models.PROTECT)
    municipality            = models.ForeignKey(Municipality, on_delete=models.PROTECT,verbose_name=_('Municipality'))
    choices_approval        = (
                                   ('Approved', _('Approved')),
                                   ('Not Approved', _('Not Approved'))
                               )
    firm_name               = models.CharField(max_length=255,verbose_name=_('Firm name'))
    contact_number = models.CharField(verbose_name=_('Contact Number'),max_length=20,default=0)

    pan_no                  = models.CharField(verbose_name=_('PAN no'),null=True,blank=True,max_length=20)
    vat_no                  = models.CharField(verbose_name=_('VAT no'),null=True,blank=True,max_length=20)
    registration_no         = models.CharField(verbose_name=_('Registration Number'),null=True,blank=True,max_length=20)
    
    ward                    = ChainedForeignKey(Ward,chained_field="municipality",
                                        chained_model_field="municipality",
                                        on_delete=models.PROTECT,
                                        auto_choose=True,
                                        verbose_name=_('Ward'))  
    tole                    = models.CharField(verbose_name=_('Tole'),max_length=150)
    registered_place        = models.CharField(max_length=20, verbose_name=_('Jaari Jilla'))
    choices_darta                 = (
                                    ('Gharelu',_('Gharelu')),
                                    ('Banijya',_('Banijya'))
                                )
    anya_darta              = models.CharField(choices=choices_darta,max_length=50,blank=True,null=True,verbose_name=_('Registered as'))
    firm_registration_proof = models.ImageField(upload_to=company_location, verbose_name=_('Firm Registration Proof'))

    sector           = ChainedForeignKey(Sector,chained_field="municipality",
                                        chained_model_field="municipality",
                                        on_delete=models.PROTECT,
                                        auto_choose=True,
                                        verbose_name=_('Sector'))

    karyakram           = ChainedForeignKey(Karyakram,
                                               chained_field="sector",
                                               chained_model_field="sector",
                                               on_delete=models.PROTECT,
                                                   auto_choose=True,
                                                   verbose_name=_('Karyakram'))        
    
    ward_sifaris            = models.ImageField(upload_to=company_location, verbose_name=_('Ward Sifaris'))
    prastavan               = models.ImageField(upload_to=company_location, verbose_name=_('Upload Prastavan'))

    approval                = models.CharField(choices=choices_approval, default='Not Approved', max_length=14,verbose_name=_('Approval'))
    created             = models.DateField(verbose_name=_('created'),auto_now_add=True,auto_now=False)
    updated             = models.DateField(verbose_name=_('updated'),auto_now=True)

    def __str__(self):
        return f'{self.firm_name}-{self.registration_no}-{self.approval}'

    class Meta:
        db_table='Anudan_Company'
        verbose_name = _('Anudan Company')
        verbose_name_plural = _('Anudan Company')



class Medicine(models.Model):
    name=models.CharField(verbose_name=_('Name'),max_length=150)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'Medicine'
        verbose_name=_('Medicine')
        verbose_name_plural = _('Medicines')


class MedicineRequest(models.Model):
    municipality    =   models.ForeignKey(Municipality,on_delete=models.DO_NOTHING,verbose_name=_('Municipality'))
    name    = models.CharField(verbose_name=_('Name'),max_length=150)
    contact_number = models.CharField(verbose_name=_('Contact Number'),max_length=10)
    
    ward                    = ChainedForeignKey(Ward,chained_field="municipality",
                                        chained_model_field="municipality",
                                        on_delete=models.PROTECT,
                                        auto_choose=True,
                                        verbose_name=_('Ward'))   

    tole    = models.CharField(verbose_name=_('Tole'),max_length=150)
    created             = models.DateField(verbose_name=_('created'),auto_now_add=True,auto_now=False)
   


    def __str__(self):
        return f'{self.ward}-{self.tole}-{self.name}'

    class Meta:
        db_table = 'Medicine_Request'
        verbose_name =_('Medicine Request')
        verbose_name_plural = _('Medicine Request')


class MedicineRequested(models.Model):
    requested_by = models.ForeignKey(MedicineRequest,on_delete=models.CASCADE,verbose_name=_('Requested By'),related_name='Medicines_Requested')
    medicine    = models.ForeignKey(Medicine,verbose_name=_('Medicine'),max_length=150,related_name='Medicines_Requested',on_delete=models.CASCADE)
    quantity    = models.PositiveSmallIntegerField(_('Quantity'),default=1)

    def __str__(self):
        return f'{self.medicine.name} requested by {self.requested_by.name} from {self.requested_by.tole} of {self.requested_by.municipality.name}'

