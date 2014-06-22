from __future__ import division
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fiddlr.settings")
from home.models import *
import random

an = ('Dale Neverknow', 'Leo Del Lahey Hy', 'Miss Inga Tooth',
      'Harriet Knight', 'Ike and Zeke Leerly', 'Deepak Tumuch',
      'Meg Meehan Hoffa', 'Ariel Payne Diaz', 'Althea Around',
      'Diana Boredom',)


typs = {'art': {
    'music': {
        'classical': {
            'renaissance': {},
            'baroque': {},
            'classical': {},
            'romantic': {},
            '20th century': {},
            'atonal': {},
            'minimalist': {},
        },
        'jazz': {
            'bebop': {},
            'hard bop': {},
            'fusion': {},
            'blues': {},
            'swing': {},
        },
        'folk': {},
        'classics': {},
        'latin': {},
    },
    'dance': {
        'ballet': {}, 
        'tango': {},
    },
    'theater': {
        'musical': {},
        'shakespearean': {},
    },
    'film': {},
    'visual': {
        'painting': {},
        'drawing': {},
        'calligraphy': {},
    },
}}
    

def make():
    artist_count = 10
    venue_count = 10
    event_count = 10


    print 'users'
    u = [User(username='ap' + str(x), password='1234',
              is_staff=False, is_active=True, is_superuser=False)
         for x in range(artist_count)]
    for i in range(artist_count):
        u[i].save()
    

    print 'profiles'
    p = [Fiprofile(user=usr) for usr in u]
    for i in range(artist_count):
        p[i].save()


    print 'artypes'
    def createArtype( typdict, parent ):
        for typname in typdict:
            typ = Artype(name=typname).save()
            if parent:
                typ.roots.add(parent)
            createArtype(typdict[typname], typ)
    createArtype(typs, None)


    print 'artists'
    a = [Artist(name='Artist '+str(x)) for x in range(artist_count)]
    for i in range(artist_count):
        a[i].save()
        a[i].members.add(u[i])
        tyname = random.choice(list(typs.keys()))
        a[i].artypes.add(Artype.objects.get(name=tyname))


    print 'geocoordinates'
    point_a = (40.758426, -73.992646) #9th & 42nd
    point_b = (40.801640, -73.961118) #9th & 110th
    lat_inc = (point_b[0] - point_a[0]) / venue_count
    lon_inc = (point_b[1] - point_a[1]) / venue_count
    geo = [Geocoordinates(latitude=point_a[0] + x*lat_inc,
                          longitude=point_a[1] + x*lon_inc)
           for x in range(venue_count)]
    for i in range(venue_count):
        geo[i].save()


    print 'venues'
    v = [Venue(name='Venue ' + str(x), geocoordinates=geo[x]) 
         for x in range(venue_count)]
    for i in range(venue_count):
        v[i].save()


    print 'events'
    e = [Event(name='Event ' + str(x), venue=v[x])
         for x in range(event_count)]
    for i in range(event_count):
        e[i].save()
        e[i].artists.add(a[i], a[(i+5)%artist_count])




if __name__ == "__main__":
    make()

