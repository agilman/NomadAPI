from rest_framework import serializers
from django.contrib.auth.models import User
from nomadapp.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk','username']

class AdventureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adventure
        fields= ['id','name','advType','advStatus']

class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields= ['id','name']

class PhotoMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoMeta
        fields = ['photo','lat','lng','ts']

class PhotoSerializer(serializers.ModelSerializer):
    meta = PhotoMetaSerializer(source='photometa')

    class Meta:
        model = Photo
        fields = ['id','caption','uploadTime','meta']
