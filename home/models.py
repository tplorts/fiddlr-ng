from django.db import models
from django.contrib.auth.models import User



class Fiprofile( models.Model ):
    user = models.OneToOneField(User)
    email_verified = models.BooleanField( default=False )
    picture = models.ForeignKey( 'Picture', null=True, blank=True )
    favorites = models.ManyToManyField( 'Fithing', blank=True, related_name='fans' )
    autovocated = models.ManyToManyField('Fithing', blank=True, related_name='vocatees')

    def __unicode__(self):
        return unicode(self.user)

    def favorite_artists(self):
        return [f.artist for f in self.favorites.all() if f.is_artist()]
    def favorite_venues(self):
        return [f.venue for f in self.favorites.all() if f.is_venue()]
    def favorite_events(self):
        return [f.event for f in self.favorites.all() if f.is_event()]

    def autovocated_artists(self):
        return [f.artist for f in self.autovocated.all() if f.is_artist()]
    def autovocated_venues(self):
        return [f.venue for f in self.autovocated.all() if f.is_venue()]
    def autovocated_events(self):
        return [f.event for f in self.autovocated.all() if f.is_event()]


class Fithing( models.Model ):
    name = models.CharField( max_length=80 )
    brief = models.CharField( max_length=200, blank=True )
    about = models.TextField( blank=True )

    website = models.URLField( blank=True )
    email = models.EmailField( max_length=254, blank=True )
    phone = models.CharField( max_length=20, blank=True )
    
    # Set of pictures will be accessible but that relation
    # is defined in the Picture model.
    logo = models.ForeignKey( 'Picture', null=True, blank=True, related_name='+' )
    cover = models.ForeignKey( 'Picture', null=True, blank=True, related_name='+' )
    
    is_official = models.BooleanField( default=False )
    is_public = models.BooleanField( default=False )

    def __unicode__(self):
        return self.name

    def is_artist(self):
        return hasattr(self, 'artist')
    def is_venue(self):
        return hasattr(self, 'venue')
    def is_event(self):
        return hasattr(self, 'event')


class Artist( Fithing ):
    members = models.ManyToManyField( User, blank=True )
    sponsors = models.ManyToManyField( 'Sponsor', blank=True )
    artypes = models.ManyToManyField( 'Artype', blank=True )


class Venue( Fithing ):
    managers = models.ManyToManyField( User, blank=True )
    address = models.CharField( max_length=200, blank=True )
    geocoordinates = models.OneToOneField( 'Geocoordinates', null=True, blank=True )
    venue_type = models.ForeignKey( 'VenueType', null=True, blank=True )
    event_types = models.ManyToManyField( 'EventType', blank=True )


class Event( Fithing ):
    venue = models.ForeignKey( 'Venue', null=True, blank=True )
    artists = models.ManyToManyField( 'Artist', blank=True )
    sponsors = models.ManyToManyField( 'Sponsor', blank=True )

    start = models.DateTimeField( null=True, blank=True )
    end = models.DateTimeField( null=True, blank=True )
    iterations = models.TextField( blank=True )

    is_reservation_required = models.BooleanField( default=False )


class Sponsor( Fithing ):
    managers = models.ManyToManyField( User, blank=True )


class Artype( models.Model ):
    name = models.CharField( max_length=80 )
    roots = models.ManyToManyField( 'Artype', related_name='branches', blank=True )

    def __unicode__(self):
        return self.name


class VenueType( models.Model ):
    name = models.CharField( max_length=80 )
    event_types = models.ManyToManyField( 'EventType' )

    def __unicode__(self):
        return self.name


class EventType( models.Model ):
    name = models.CharField( max_length=80 )

    def __unicode__(self):
        return self.name


class Price( models.Model ):
    amount = models.DecimalField( max_digits=12, decimal_places=4 )
    event = models.ForeignKey( 'Event' )
    category = models.ForeignKey( 'PriceCategory', null=True, blank=True )

    def __unicode__(self):
        s = '$' + unicode(self.amount)
        if self.category:
            s = unicode(self.category) + ': ' + s
        return s


class PriceCategory( models.Model ):
    name = models.CharField( max_length=80 )

    def __unicode__(self):
        return self.name


class Picture( models.Model ):
    url = models.URLField()
    of = models.ForeignKey( 'Fithing', null=True, blank=True )
    ordinal = models.FloatField( null=True, blank=True )

    def __unicode__(self):
        return self.url.split('/')[-1]


class Geocoordinates( models.Model ):
    latitude = models.DecimalField( max_digits=9, decimal_places=6 )
    longitude = models.DecimalField( max_digits=9, decimal_places=6 )

    def __unicode__(self):
        return '['+unicode(self.latitude)+', '+unicode(self.longitude)+']'

    def id(self):
        return self.pk
