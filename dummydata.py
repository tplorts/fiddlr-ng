from __future__ import division
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fiddlr.settings")
from home.models import *


an = ('Dale Neverknow', 'Leo Del Lahey Hy', 'Miss Inga Tooth',
      'Harriet Knight', 'Ike and Zeke Leerly', 'Deepak Tumuch',
      'Meg Meehan Hoffa', 'Ariel Payne Diaz', 'Althea Around',
      'Diana Boredom',)


def make():
    u = [User(name='Artist Person ' + str(x),
              email='artistperson' + str(x) + '@nothing.net')
         for x in range(10)]
    for i in range(10):
        u[i].save()


    a = [Artist(name=anx) for anx in an]
    for i in range(10):
        a[i].save()
        a[i].members.add(u[i])


    point_a = (40.758426, -73.992646) #9th & 42nd
    point_b = (40.801640, -73.961118) #9th & 110th
    lat_inc = (point_b[0] - point_a[0]) / 10
    lon_inc = (point_b[1] - point_a[1]) / 10
    geo = [Geocoordinates(latitude=point_a[0] + x*lat_inc,
                          longitude=point_a[1] + x*lon_inc)
           for x in range(10)]
    for i in range(10):
        geo[i].save()


    v = [Venue(name='Venue ' + str(x),
               geocoordinates=geo[x]) 
         for x in range(10)]
    for i in range(10):
        v[i].save()


    e = [Event(name='Event ' + str(x),
               venue=v[x])
         for x in range(10)]
    for i in range(10):
        e[i].save()
        e[i].artists.add(a[i])




if __name__ == "__main__":
    make()

