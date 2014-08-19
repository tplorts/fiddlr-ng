from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id','address','neighborhood','zipcode',
                  'latitude','longitude')


class CreoTieSerializer(serializers.ModelSerializer):
    locationExpanded = LocationSerializer(source='location')
    class Meta:
        model = Creo
        fields = ('id','creotype','name','locationExpanded')


class CreoSerializer(serializers.ModelSerializer):
    coverURL = serializers.Field(source='coverURL')
    logoURL = serializers.Field(source='logoURL')
    locationExpanded = LocationSerializer(source='location')
    ties = CreoTieSerializer(many=True)
    class Meta:
        model = Creo
        fields = ('id','creotype','name','brief','about',
                  'cover','coverURL','logo','logoURL',
                  'location','website','email','phone','genres',
                  'isPublic','isOfficial','ties','locationExpanded',
                  'start', 'end',)
