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


class CreoSerializer(serializers.ModelSerializer):
    coverURL = serializers.Field(source='coverURL')
    logoURL = serializers.Field(source='logoURL')
    # location = LocationSerializer()
    locationInfo = LocationSerializer(source='location')
    class Meta:
        model = Creo
        fields = ('id','creotype','name','brief','about',
                  'cover','coverURL','logo','logoURL',
                  'location','website','email','phone','genres',
                  'isPublic','isOfficial','ties','locationInfo')



class EventVenueSerializer(CreoSerializer):
    class Meta(CreoSerializer.Meta):
        fields = ('id', 'name', 'website', 'logo', 'location')

class EventArtistsSerializer(CreoSerializer):
    class Meta(CreoSerializer.Meta):
        fields = ('id', 'name', 'brief')

class EventSponsorsSerializer(CreoSerializer):
    class Meta(CreoSerializer.Meta):
        fields = ('id', 'name', 'logo')

class EventListSerializer(CreoSerializer):
    # venues = EventVenueSerializer()
    # artists = EventArtistsSerializer(many=True)
    # sponsors = EventSponsorsSerializer(many=True)
    class Meta(CreoSerializer.Meta):
        fields = ('id', 'name', 'brief', 'venues', 'logo', 'start',
                  'end', 'artists', 'sponsors')
