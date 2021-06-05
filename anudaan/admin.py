from django.contrib import admin
from .models import Karyakram,Samagri,AnudanPerosnal

# Register your models here.
@admin.register(Karyakram)
class KaryakramAdmin(admin.ModelAdmin):
    list_display=['id','name']


@admin.register(Samagri)
class SamagriAdmin(admin.ModelAdmin):
    list_display=['id','name','karyakram']
    list_filter=['karyakram']

@admin.register(AnudanPerosnal)
class AnudanAdmin(admin.ModelAdmin):
    list_display=['id','name','ward','Tole','NagriktaNumber','JariJilla','karyakram','NagriktaFront','NagriktaBack','samagri','approval']
    list_filter=['approval','ward','Tole','JariJilla','karyakram','samagri']
