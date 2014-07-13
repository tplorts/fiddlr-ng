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


class FingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fing

class ArtistSerializer(FingSerializer):
    class Meta(FingSerializer.Meta):
        fields = ('id','name','brief')



class EventVenueSerializer(FingSerializer):
    location = LocationSerializer()
    class Meta(FingSerializer.Meta):
        fields = ('id', 'name', 'website', 'logo', 'location')

class EventArtistsSerializer(FingSerializer):
    class Meta(FingSerializer.Meta):
        fields = ('id', 'name', 'brief')

class EventSponsorsSerializer(FingSerializer):
    class Meta(FingSerializer.Meta):
        fields = ('id', 'name', 'logo')

class EventListSerializer(FingSerializer):
    venue = EventVenueSerializer()
    artists = EventArtistsSerializer(many=True)
    sponsors = EventSponsorsSerializer(many=True)
    class Meta(FingSerializer.Meta):
        fields = ('id', 'name', 'brief', 'venue', 'logo', 'start',
                  'end', 'artists', 'sponsors')
