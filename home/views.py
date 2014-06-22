from django.shortcuts import render
from django.core.serializers import serialize
from django.db.models import Q
from django import forms
from fiddlr import settings
from models import *



class FiddlrSearchForm( forms.Form ):
    what = forms.CharField()
    where = forms.CharField(required=False)



def renderView( request, template, context={} ):
    context.update({
        'isProduction': settings.isProduction,
        'useLESS': settings.TEMPLATE_DEBUG,
    })
    return render( request, template, context )


def renderPage( request, template, context={} ):
    if '/' not in template:
        section = None
        page = template
    else:
        section,_,page = template.partition('/')
    if 'search_form' not in context:
        # if the search form wasn't already set by the
        # search view, supply it for any page's header
        context.update({'search_form': FiddlrSearchForm()})
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
    events = Event.objects.order_by('-name')
    eventsJSON = serialize(
        'json', 
        events, 
        relations={
            'venue': {
                'relations': {
                    'geocoordinates': {'extras': ('id',)}
                },
                'extras': ('name',),
            },
        },
        extras=('name', 'brief',)
    )
    return renderPage(q, 'explore/map', {
        'gmaps_api_key': settings.gmaps_api_key,
        'featured_events': events,
        'featured_events_json': eventsJSON,
    })

def explore_profile(q):
    return renderPage(q, 'explore/profile/root')

def explore_profile_events(q):
    u = User.objects.get(pk=76)
    return renderPage(q, 'explore/profile/events', {
        'favorite_events': u.favorite_events(),
    })

def explore_profile_artists(q):
    u = User.objects.get(pk=76)
    return renderPage(q, 'explore/profile/artists', {
        'favorite_artists': u.favorite_artists(),
    })

def explore_profile_venues(q):
    u = User.objects.get(pk=76)
    return renderPage(q, 'explore/profile/venues', {
        'favorite_venues': u.favorite_venues(),
    })

def explore_profile_forMe(q):
    return renderPage(q, 'explore/profile/for-me')
def explore_profile_nearMe(q):
    return renderPage(q, 'explore/profile/near-me')
def explore_profile_browse(q):
    return renderPage(q, 'explore/profile/browse')


def create(q):
    return renderPage(q, 'create/root')

def connect(q):
    return renderPage(q, 'connect/root')


def artist_page(q, artist_id):
    return renderPage(q, 'artist/page', {
        'artist': Artist.objects.get(pk=artist_id),
    })

def venue_page(q, venue_id):
    return renderPage(q, 'venue/page', {
        'venue': Venue.objects.get(pk=venue_id),
    })

def event_page(q, event_id):
    return renderPage(q, 'event/page', {
        'event': Event.objects.get(pk=event_id),
    })


def alerts(q):
    return renderPage(q, 'alerts', {
        'alerts': ('stuff',)*10,
    })


def search(q):
    c = {}
    if q.method == 'POST':
        form = FiddlrSearchForm( q.POST )
        what = form.data['what']
        where = form.data['where']
        query = Q(name__icontains=what) | Q(brief__icontains=what)
        results = Fidentity.objects.filter(query)
        c.update({'search_results': results})
    else:
        form = FiddlrSearchForm()
    c.update({'search_form': form})
    return renderPage(q, 'search', c)


def about(q):
    return renderPage(q, 'auxiliary/about')

def copyrightView(q):
    return renderPage(q, 'auxiliary/copyright')

def helpView(q):
    return renderPage(q, 'auxiliary/help')

def adsView(q):
    return renderPage(q, 'auxiliary/ads')

