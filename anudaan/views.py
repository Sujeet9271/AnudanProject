from django.shortcuts import render
from .models import AnudanPerosnal, Karyakram, Samagri

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers, status

from .serializers import KaryakramSerialzier,SamagriSerializer,AnudanPersonalSerializer

@api_view(['GET','POST'])
def create_karyakram(request):
    if request.method=='GET':
        qs = Karyakram.objects.all()
        serializer = KaryakramSerialzier(qs,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        data = request.data
        serializer = KaryakramSerialzier(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def create_samagri(request):
    if request.method=='GET':
        qs = Samagri.objects.all()
        serializer = SamagriSerializer(qs,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        data = request.data
        serializer = SamagriSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_anudan(request):
    data={
    'name'           : request.data['name'],
    'ward'           : request.data['ward'],
    'Tole'           : request.data['Tole'],
    'NagriktaNumber' : request.data['NagriktaNumber'],
    'JariJilla'      : request.data['JariJilla'],
    'karyakram'      : request.data['karyakram'],
    'NagriktaFront'  : request.data['NagriktaFront'],
    'NagriktaBack'   : request.data['NagriktaBack'],
    'samagri'        : request.data['samagri'],
    }
    
    serializer = AnudanPersonalSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
