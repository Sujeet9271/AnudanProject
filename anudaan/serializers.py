from .models import Karyakram,Samagri,AnudanPerosnal
from rest_framework import serializers


class KaryakramSerialzier(serializers.ModelSerializer):
    
    class Meta:
        model = Karyakram
        fields = '__all__'

class SamagriSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Samagri
        fields = ['id','name','karyakram','karyakram_name']

class AnudanPersonalSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnudanPerosnal
        fields = ['id','name','ward','Tole','NagriktaNumber','JariJilla','karyakram','NagriktaFront','NagriktaBack','samagri','approval']