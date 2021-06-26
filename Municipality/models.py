from django.db import models
from django.utils.translation import gettext_lazy as _





# Create your models here.
class Municipality(models.Model):
    name            = models.CharField(verbose_name=_('Name'),max_length=150)
    contact_number  = models.CharField(verbose_name=_('Contact Number'),max_length=10,unique=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table='Municipality'
        verbose_name = _('Municipality')
        verbose_name_plural = _('Municipalities')

class Sector(models.Model):
    municipality = models.ForeignKey(Municipality,verbose_name=_('Municipality'), on_delete=models.CASCADE)
    name = models.CharField(max_length=150,verbose_name=_('Name'))

    def __str__(self):
        return f"{self.name}-{self.municipality.name}"

    class Meta:
        db_table='Sector'
        verbose_name = _('Sector')
        verbose_name_plural = _('Sectors')


class Ward(models.Model):
    municipality = models.ForeignKey(Municipality,verbose_name=_('Municipality'), on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Name'),max_length=150)

    def __str__(self):
        return f'{self.name}-{self.municipality.name}'

    class Meta:
        db_table='Ward'
        verbose_name = _('Ward')
        verbose_name_plural = _('Ward')
