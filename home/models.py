from django.db import models



class User( models.Model ):
    name = models.CharField( max_length=50, blank=True )
    email = models.EmailField( max_length=254 )
    password = models.CharField( max_length=50, blank=True )
    picture = models.ForeignKey( 'Picture', null=True, blank=True )
    favorites = models.ManyToManyField( 'Fidentity', blank=True )

    def __unicode__(self):
        if self.name and len(self.name) > 0:
            return self.name
        else:
            return self.email


class Fidentity( models.Model ):
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


class Artist( Fidentity ):
    members = models.ManyToManyField( 'User' )
    sponsors = models.ManyToManyField( 'Sponsor' )


class Venue( Fidentity ):
    managers = models.ManyToManyField( 'User' )
    address = models.CharField( max_length=200, blank=True )
    geocoordinates = models.OneToOneField( 'Geocoordinates', null=True )
    venue_type = models.ForeignKey( 'VenueType', null=True )
    event_types = models.ManyToManyField( 'EventType' )


class Event( Fidentity ):
    venue = models.ForeignKey( 'Venue', null=True )
    artists = models.ManyToManyField( 'Artist' )
    sponsors = models.ManyToManyField( 'Sponsor' )

    start = models.DateTimeField( null=True )
    end = models.DateTimeField( null=True )
    iterations = models.TextField( blank=True )

    is_reservation_required = models.BooleanField( default=False )


class Sponsor( Fidentity ):
    pass


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
    category = models.ForeignKey( 'PriceCategory', null=True )

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
    entity = models.ForeignKey( 'Fidentity', null=True )
    ordinal = models.FloatField( null=True )

    def __unicode__(self):
        return self.url.split('/')[-1]


class Geocoordinates( models.Model ):
    latitude = models.DecimalField( max_digits=9, decimal_places=6 )
    longitude = models.DecimalField( max_digits=9, decimal_places=6 )

    def __unicode__(self):
        return '['+unicode(self.latitude)+', '+unicode(self.longitude)+']'

