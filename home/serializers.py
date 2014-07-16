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
        fields = ('id', 'latitude', 'longitude')


class CreoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creo

class ArtistSerializer(CreoSerializer):
    class Meta(CreoSerializer.Meta):
        fields = ('id','name','brief')



class EventVenueSerializer(CreoSerializer):
    location = LocationSerializer()
    class Meta(CreoSerializer.Meta):
        fields = ('id', 'name', 'website', 'logo', 'location')

class EventArtistsSerializer(CreoSerializer):
    class Meta(CreoSerializer.Meta):
        fields = ('id', 'name', 'brief')

class EventSponsorsSerializer(CreoSerializer):
    class Meta(CreoSerializer.Meta):
        fields = ('id', 'name', 'logo')

class EventListSerializer(CreoSerializer):
    venue = EventVenueSerializer()
    artists = EventArtistsSerializer(many=True)
    sponsors = EventSponsorsSerializer(many=True)
    class Meta(CreoSerializer.Meta):
        fields = ('id', 'name', 'brief', 'venue', 'logo', 'start',
                  'end', 'artists', 'sponsors')
