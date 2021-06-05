from django.db import models

class Karyakram(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}'


class Samagri(models.Model):
    karyakram = models.ForeignKey(Karyakram,on_delete=models.CASCADE, related_name='samagri')
    name      = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.name}-{self.karyakram}'

    def karyakram_name(self):
        return self.karyakram.name

    class Meta:
        ordering=['karyakram']


def location(instance,filename):
    return f"{instance.name}/{filename}"

class AnudanPerosnal(models.Model):
    choices_approval = (
        ('Approved',('Approved')),
       ('Not Approved', ('Not Approved'))
    )
    name           = models.CharField(max_length=255)
    ward           = models.PositiveIntegerField(max_length=2)
    Tole           = models.CharField(max_length=255)
    NagriktaNumber = models.PositiveBigIntegerField(max_length=12,verbose_name='Nagrikta Number')
    JariJilla      = models.CharField(max_length=20, verbose_name='Jaari Jilla')
    karyakram      = models.ForeignKey(Karyakram,on_delete=models.CASCADE,)
    NagriktaFront  = models.ImageField(upload_to=location,verbose_name='Nagrikta Front Photo')
    NagriktaBack   = models.ImageField(upload_to=location,verbose_name='Nagrikta Back Photo')
    samagri        = models.ForeignKey(Samagri,on_delete=models.CASCADE)
    approval       = models.CharField(choices=choices_approval,default='Not Approved',max_length=14)

    def __str__(self):
        return f'{self.name}-{self.karyakram}-{self.samagri}-{self.approval}'

class AnudanCompany(models.Model):
    choices_approval = (
        ('Approved',('Approved')),
       ('Not Approved', ('Not Approved'))
    )
    firm_name           = models.CharField(max_length=255)
    Pan_No           = models.PositiveIntegerField(max_length=2)
    Vat_No           = models.CharField(max_length=255)
    Registration_No = models.PositiveBigIntegerField(max_length=12,verbose_name='Registration Number')
    ward           = models.PositiveIntegerField(max_length=2)
    Tole           = models.CharField(max_length=255)
    
    JariJilla      = models.CharField(max_length=20, verbose_name='Jaari Jilla')
    karyakram      = models.ForeignKey(Karyakram,on_delete=models.CASCADE,)
    NagriktaFront  = models.ImageField(upload_to=location,verbose_name='Nagrikta Front Photo')
    NagriktaBack   = models.ImageField(upload_to=location,verbose_name='Nagrikta Back Photo')
    samagri        = models.ForeignKey(Samagri,on_delete=models.CASCADE)
    approval       = models.CharField(choices=choices_approval,default='Not Approved',max_length=14)

    def __str__(self):
        return f'{self.name}-{self.karyakram}-{self.samagri}-{self.approval}'