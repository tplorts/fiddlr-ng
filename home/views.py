from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib import auth
from django.contrib.auth.views import login as auth_login_view
from django.contrib.auth.models import User, Group
from django.core.serializers import serialize
from django.db.models import Q
from django import forms
from rest_framework import viewsets, authentication
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from fiddlr import settings
from serializers import UserSerializer, GroupSerializer
from permissions import JustMe
from models import *
from datetime import datetime, timedelta, date, time


class UserExistsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, username, format=None):
        exists = User.objects.filter(username=username).exists()
        return Response(exists)


class SetPasswordView(APIView):
    permission_classes = (JustMe,)

#    def post(self, request, format=None):

        


class IsEmailVerifiedView(APIView):
    permission_classes = (JustMe,)

    def post(self, request, format=None):
        try:
            isVerified = request.user.fiprofile.email_verified
        except Fiprofile.DoesNotExist:
            isVerified = False
        return Response(isVerified)



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer





class FiddlrSearchForm( forms.Form ):
    what = forms.CharField()
    where = forms.CharField(required=False)



def injectDefaultContext( template, context ):
    if '/' not in template:
        section = None
        page = template
    else:
        section,_,page = template.partition('/')
    if '.' in page:
        page,_,_ = page.partition('.')
    
    if 'search_form' not in context:
        # if the search form wasn't already set by the
        # search view, supply it for any page's header
        context.update({'search_form': FiddlrSearchForm()})

    context.update({
        'isProduction': settings.isProduction,
        'useLESS': settings.TEMPLATE_DEBUG,
        'section': section,
        'page': page,
        'ngCDN': 'http://ajax.googleapis.com/ajax/libs/angularjs/',
        'ngVersion': '1.3.0-beta.13/',
        'thetime': datetime.now(),
    })

def renderView( request, template, context={} ):
    injectDefaultContext( template, context )
    return render( request, template, context )

def renderPage( request, template, context={} ):
    return renderView( request, template+'.html', context )




def front(q):
    now = datetime.utcnow().time()
    # Window of Good Morning Gaby: [8:48, 8:52)
    time4gaby = now.hour==12 and now.minute in range(48, 52)
    return renderPage(q, 'front', {
        'time4gabymorning': time4gaby
    })



def login(q):
    context = {}
    injectDefaultContext( 'login', context )
    return auth_login_view( q, extra_context=context )


secret_agents = ('the1&onlyGABY', 'H@NN@H',)
def signup(q):
    if q.method == 'POST':
        said = q.POST['secret_agent_id']
        if said not in secret_agents:
            return HttpResponseRedirect('/access-denied/')
        uname = q.POST['username']
        email = q.POST['email']
        pword = q.POST['password']
        User.objects.create_user(uname, email, pword)
        #TODO: handle failure to create user
        user = auth.authenticate(username=uname, password=pword)
        if user is not None and user.is_active:
            profile = Fiprofile(user=user)
            profile.save()
            auth.login(q, user)
            return HttpResponseRedirect('/account/')

    return HttpResponseRedirect(q.META.get('HTTP_REFERER'))


def account(q):
    return renderPage(q, 'registration/account')



event_lists = {
    'featured': 'Featured Events',
    'for-you': 'Events For You',
    'near-you': 'Events Near You',
    'happening-now': 'Events Happening Now',
    'fiddlr-events': 'fiddlr events',
}
event_view_types = ('list', 'map')

def explore(q):
    return renderPage(q, 'explore/explore-home')

def explore_events(q, list_name, view_type):
    if list_name not in event_lists:
        raise Http404
    if view_type not in event_view_types:
        raise Http404

    if not q.user.is_authenticated():
        events = []
    elif list_name == 'featured':
        events = Event.objects.filter( is_featured=True )
    elif list_name == 'near-you':
        events = Event.objects.all()
    elif list_name == 'for-you':
        events = q.user.fiprofile.autovocated_events()
    elif list_name == 'happening-now':
        hasnt_ended = Q( end__gt=datetime.now() )
        starts_by_tomorrow = Q( start__lt=date.today()+timedelta(days=2) )
        # Why +2 days? Read the warning about dates & datetimes.
        # To include tomorrow, set upper bound to 0:00 after tomorrow.
        # https://docs.djangoproject.com/en/1.6/ref/models/querysets/#range
        events = Event.objects.filter(
            hasnt_ended & starts_by_tomorrow
        ).order_by('end')
    elif list_name == 'fiddlr-events':
        events = []

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

    return renderPage(q, 'explore/events/'+view_type, {
        'events': events,
        'list_name': list_name,
        'list_title': event_lists[list_name],
        'gmaps_api_key': settings.gmaps_api_key,
#        'time2boogie': list_name == 'for-you',
        'events_json': eventsJSON,
    })
        

def explore_events_list(q, list_name):
    return explore_events(q, list_name, 'list')

def explore_events_map(q, list_name):
    return explore_events(q, list_name, 'map')



def explore_profile(q):
    return renderPage(q, 'explore/profile/root')

def explore_profile_events(q):
    return renderPage(q, 'explore/profile/events', {
        'favorite_events': [],
    })

def explore_profile_artists(q):
    return renderPage(q, 'explore/profile/artists', {
        'favorite_artists': [],
    })

def explore_profile_venues(q):
    return renderPage(q, 'explore/profile/venues', {
        'favorite_venues': [],
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
        results = Fithing.objects.filter(query)
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



if not settings.isProduction:
    def test404(q):
        return render(q, '404.html', {})
    def test500(q):
        return render(q, '500.html', {})

