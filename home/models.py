from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from utilities import *


class NamedModel():
    def __unicode__(self):
        return self.name


FypeArtist = 1
FypeVenue = 2
FypeSponsor = 3
FypeEvent = 4
FypeTour = 5
FypeChoices = (
    (FypeArtist, 'Artist'),
    (FypeVenue, 'Venue'),
    (FypeSponsor, 'Sponsor'),
    (FypeEvent, 'Event'),
    (FypeTour, 'Tour'),
)

ValidFypes = range(FypeChoices[0][0], FypeChoices[-1][0]+1)

QArtist = Q(fype=FypeArtist)
QVenue = Q(fype=FypeVenue)
QSponsor = Q(fype=FypeSponsor)
QEvent = Q(fype=FypeEvent)
QTour = Q(fype=FypeTour)



class Fuser( models.Model ):
    user = models.OneToOneField(User)
    pseudonym = models.CharField( max_length=50, blank=True )
    isEmailVerified = models.BooleanField( default=False )
    picture = models.ForeignKey( 'Picture', null=True, blank=True )
    favorites = models.ManyToManyField( 'Fing', blank=True,
                                        related_name='fans' )
    autovocated = models.ManyToManyField('Fing', blank=True,
                                         related_name='vocatees')

    def __unicode__(self):
        return unicode(self.user)

    def favoriteArtists(self):
        return self.favorites.filter(QArtist)
    def favoriteVenues(self):
        return self.favorites.filter(QVenue)
    def favoriteEvents(self):
        return self.favorites.filter(QEvent)

    def autovocatedArtists(self):
        return self.autovocated.filter(QArtist)
    def autovocatedVenues(self):
        return self.autovocated.filter(QVenue)
    def autovocatedEvents(self):
        return self.autovocated.filter(QEvent)

    def isFollowing(self, fingId):
        return self.favorites.filter(pk=fingId).count() == 1


class ArtistModelManager( models.Manager ):
    def get_queryset(self):
        return super(ArtistModelManager, self).get_queryset().filter(QArtist)
class VenueModelManager( models.Manager ):
    def get_queryset(self):
        return super(VenueModelManager, self).get_queryset().filter(QVenue)
class SponsorModelManager( models.Manager ):
    def get_queryset(self):
        return super(SponsorModelManager, self).get_queryset().filter(QSponsor)
class EventModelManager( models.Manager ):
    def get_queryset(self):
        return super(EventModelManager, self).get_queryset().filter(QEvent)


class Fing( models.Model, NamedModel ):
    fype = models.SmallIntegerField( choices=FypeChoices )
    name = models.CharField( max_length=60, blank=True )
    brief = models.CharField( max_length=100, blank=True )
    about = models.TextField( blank=True )
    location = models.ForeignKey( 'Location', null=True, blank=True,
                                  related_name='fings' )
    website = models.URLField( blank=True )
    email = models.EmailField( max_length=254, blank=True )
    phone = models.CharField( max_length=20, blank=True )
    logo = models.ForeignKey( 'Picture', null=True, blank=True, 
                              related_name='+' )
    cover = models.ForeignKey( 'Picture', null=True, blank=True, 
                               related_name='+' )
    isOfficial = models.BooleanField( default=False )
    isPublic = models.BooleanField( default=False )
    start = models.DateTimeField( null=True, blank=True )
    end = models.DateTimeField( null=True, blank=True )
    isReservationRequired = models.BooleanField( default=False )
    managers = models.ManyToManyField( Fuser, related_name='fings' )
    ties = models.ManyToManyField( 'self' )
    fategories = models.ManyToManyField( 'Fategory', blank=True,
                                         related_name='fings' )

    objects = models.Manager()

    artists = ArtistModelManager()
    venues = VenueModelManager()
    sponsor = SponsorModelManager()
    events = EventModelManager()

    # I make these just for the convenience in template authoring
    def isArtist(self):
        return self.fype == FypeArtist
    def isVenue(self):
        return self.fype == FypeVenue
    def isSponsor(self):
        return self.fype == FypeSponsor
    def isEvent(self):
        return self.fype == FypeEvent
    def isTour(self):
        return self.fype == FypeTour


    def venue(self):
        if self.venues.count() > 0:
            return self.venues.all()[0]
        return None

    def isManager(self, fuserId):
        return self.managers.filter(pk=fuser).count() == 1


class Fategory( models.Model, NamedModel ):
    fype = models.SmallIntegerField( choices=FypeChoices )
    name = models.CharField( max_length=60 )
    roots = models.ManyToManyField( 'self', symmetrical=False,
                                    related_name='kin' )


class Price( models.Model ):
    amount = models.DecimalField( max_digits=12, decimal_places=4 )
    what = models.ForeignKey( Fing, related_name='prices' )
    category = models.ForeignKey( 'PriceCategory', 
                                  null=True, blank=True )

    def __unicode__(self):
        s = '$' + unicode(self.amount)
        if self.category:
            s = unicode(self.category) + ': ' + s
        return s


class PriceCategory( models.Model, NamedModel ):
    name = models.CharField( max_length=80 )


class Picture( models.Model ):
    url = models.URLField()
    caption = models.CharField( max_length=100, blank=True )
    ordinal = models.FloatField( null=True, blank=True )

    def __unicode__(self):
        return self.caption


class PictureAlbum( models.Model, NamedModel ):
    name = models.CharField( max_length=80, blank=True )
    about = models.TextField( blank=True )
    pictures = models.ManyToManyField( Picture, blank=True, 
                                       related_name='albums' )


class Location( models.Model ):
    address = models.CharField( max_length=100, blank=True )
    neighborhood = models.CharField( max_length=50, blank=True )
    zipcode = models.CharField( max_length=10, blank=True )
    latitude = models.DecimalField( max_digits=10, decimal_places=7, 
                                    null=True, blank=True )
    longitude = models.DecimalField( max_digits=10, decimal_places=7,
                                     null=True, blank=True )

    def __unicode__(self):
        if len(self.address) != 0:
            return self.address
        if len(self.neighborhood) != 0:
            return self.neighborhood
        if len(self.zipcode) != 0:
            return self.zipcode
        if self.latitude and self.longitude:
            return '%.7,%.7' % self.latitude, self.longitude
        return 'undefined location'

    def id(self):
        return self.pk


class Feature( models.Model ):
    fing = models.ForeignKey( Fing, related_name='featurings' )
    #TODO: things...
