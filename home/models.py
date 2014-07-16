from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from utilities import *


class NamedModel():
    def __unicode__(self):
        return self.name


CreotypeArtist = 1
CreotypeVenue = 2
CreotypeSponsor = 3
CreotypeEvent = 4
CreotypeTour = 5
CreotypeChoices = (
    (CreotypeArtist, 'Artist'),
    (CreotypeVenue, 'Venue'),
    (CreotypeSponsor, 'Sponsor'),
    (CreotypeEvent, 'Event'),
    (CreotypeTour, 'Tour'),
)

ValidCreotypes = range(CreotypeChoices[0][0], CreotypeChoices[-1][0]+1)

QArtist = Q(creotype=CreotypeArtist)
QVenue = Q(creotype=CreotypeVenue)
QSponsor = Q(creotype=CreotypeSponsor)
QEvent = Q(creotype=CreotypeEvent)
QTour = Q(creotype=CreotypeTour)


def userPictureS3Key(instance, filename):
    return '/'.join(('media', 'users', instance.username, filname))

class Uzer( models.Model ):
    user = models.OneToOneField(User)
    pseudonym = models.CharField( max_length=50, blank=True )
    isEmailVerified = models.BooleanField( default=False )
    picture = models.ImageField( upload_to=userPictureS3Key, 
                                 blank=True )
    favorites = models.ManyToManyField( 'Creo', blank=True,
                                        related_name='fans' )
    autovocated = models.ManyToManyField('Creo', blank=True,
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

    def isFollowing(self, creoId):
        return self.favorites.filter(pk=creoId).count() == 1


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


def generalS3Key(group, instance, filename):
    return '/'.join(('media', group, instance.name, filename))
def logoS3Key(instance, filename):
    return generalS3Key('logo', instance, filename)
def coverS3Key(instance, filename):
    return generalS3Key('cover', instance, filename)

class Creo( models.Model, NamedModel ):
    creotype = models.SmallIntegerField( choices=CreotypeChoices )
    name = models.CharField( max_length=60, blank=True )
    brief = models.CharField( max_length=100, blank=True )
    about = models.TextField( blank=True )
    location = models.ForeignKey( 'Location', null=True, blank=True,
                                  related_name='creos' )
    website = models.URLField( blank=True )
    email = models.EmailField( max_length=254, blank=True )
    phone = models.CharField( max_length=20, blank=True )
    logo = models.ImageField(upload_to=logoS3Key, blank=True)
    cover = models.ImageField(upload_to=coverS3Key, blank=True)
    isOfficial = models.BooleanField( default=False )
    isPublic = models.BooleanField( default=False )
    start = models.DateTimeField( null=True, blank=True )
    end = models.DateTimeField( null=True, blank=True )
    isReservationRequired = models.BooleanField( default=False )
    editors = models.ManyToManyField( Uzer, related_name='creos' )
    ties = models.ManyToManyField( 'self', blank=True )
    genres = models.ManyToManyField( 'Genre', blank=True,
                                     related_name='creos' )

    objects = models.Manager()

    artists = ArtistModelManager()
    venues = VenueModelManager()
    sponsor = SponsorModelManager()
    events = EventModelManager()

    # I make these just for the convenience in template authoring
    def isArtist(self):
        return self.creotype == CreotypeArtist
    def isVenue(self):
        return self.creotype == CreotypeVenue
    def isSponsor(self):
        return self.creotype == CreotypeSponsor
    def isEvent(self):
        return self.creotype == CreotypeEvent
    def isTour(self):
        return self.creotype == CreotypeTour


    def venue(self):
        if self.venues.count() > 0:
            return self.venues.all()[0]
        return None

    def isEditor(self, uzerId):
        return self.editors.filter(pk=uzerId).count() == 1


class Genre( models.Model, NamedModel ):
    creotype = models.SmallIntegerField( choices=CreotypeChoices )
    name = models.CharField( max_length=60 )
    roots = models.ManyToManyField( 'self', symmetrical=False,
                                    related_name='kin' )


class Price( models.Model ):
    amount = models.DecimalField( max_digits=12, decimal_places=4 )
    what = models.ForeignKey( Creo, related_name='prices' )
    category = models.ForeignKey( 'PriceCategory', 
                                  null=True, blank=True )

    def __unicode__(self):
        s = '$' + unicode(self.amount)
        if self.category:
            s = unicode(self.category) + ': ' + s
        return s


class PriceCategory( models.Model, NamedModel ):
    name = models.CharField( max_length=80 )


def albumPictureS3Key(instance, filename):
    return 'media/albums/%s/%s' % (instance.album.name, filename)

class Picture( models.Model ):
    image = models.ImageField( upload_to=albumPictureS3Key )
    album = models.ForeignKey( 'PictureAlbum', 
                               related_name='pictures' )
    caption = models.CharField( max_length=100, blank=True )
    ordinal = models.FloatField( null=True, blank=True )

    def __unicode__(self):
        return self.caption


class PictureAlbum( models.Model, NamedModel ):
    name = models.CharField( max_length=80, blank=True )
    about = models.TextField( blank=True )
    creo = models.ForeignKey( Creo, null=True, blank=True,
                              related_name='pictureAlbums' )


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
    creo = models.ForeignKey( Creo, related_name='featurings' )
    #TODO: things...
