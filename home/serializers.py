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



class GeocoordinatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geocoordinates

class EventVenueSerializer(serializers.ModelSerializer):
    geocoordinates = GeocoordinatesSerializer()

    class Meta:
        model = Venue
        fields = ('id', 'name', 'website', 'logo', 'address', 
                  'geocoordinates')

class EventArtistsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name')

class EventListSerializer(serializers.ModelSerializer):
    venue = EventVenueSerializer()
    artists = EventArtistsSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'name', 'brief', 'venue', 'logo', 'start',
                  'end', 'iterations', 'artists', 'sponsors')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
