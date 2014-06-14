from django.shortcuts import render
from django.core.serializers import serialize
from fiddlr import settings
from models import *


def renderView( request, template, context={} ):
    context.update({
        'isProduction': settings.isProduction,
        'useLESS': settings.TEMPLATE_DEBUG,
    })
    return render( request, template, context )


def renderPage( request, template, context={} ):
    if '/' in template:
        section = None
        page = template
    else:
        section,_,page = template.partition('/')
    context.update({
        'section': section,
        'page': page,
    })
    return renderView( request, template+'.html', context )


def front(q):
    return renderPage(q, 'front')


def explore(q):
    return renderPage(q, 'explore/root')

def explore_featured(q):
    return renderPage(q, 'explore/featured', {
        'featured_events': Event.objects.all(),
    })

def explore_nearYou(q):
    return renderPage(q, 'explore/near-you')
def explore_forYou(q):
    return renderPage(q, 'explore/for-you')
def explore_fiddlrEvents(q):
    return renderPage(q, 'explore/fiddlr-events')
def explore_happeningNow(q):
    return renderPage(q, 'explore/happening-now')



def explore_map(q):
    initial_markers = (
        {'id':1,
         'latitude': 40.7363114,
         'longitude': -73.9908941},
        {'id':2,
         'latitude': 40.765936,
         'longitude': -73.984026},
    )
    events = Event.objects.all()
    eventsJSON = serialize(
        'json', 
        events, 
        relations={
            'venue': {
                'relations': {
                    'geocoordinates': {'extras': ('id',)}
                }
            }
        },
        extras=('name',)
    )
    return renderPage(q, 'explore/map', {
        'gmaps_api_key': settings.gmaps_api_key,
        'initial_markers': initial_markers,
        'featured_events': events,
        'featured_events_json': eventsJSON,
    })

def create(q):
    return renderPage(q, 'create/root')

def connect(q):
    return renderPage(q, 'connect/root')



def about(q):
    return renderPage(q, 'auxiliary/about')

def copyrightView(q):
    return renderPage(q, 'auxiliary/copyright')

def helpView(q):
    return renderPage(q, 'auxiliary/help')

def adsView(q):
    return renderPage(q, 'auxiliary/ads')

