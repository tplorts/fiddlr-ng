from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib import auth
from django.contrib.auth.views import login as auth_login_view
from django.contrib.auth.models import User, Group
from django.core.serializers import serialize
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django import forms
from rest_framework import viewsets, authentication, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from fiddlr import settings
from serializers import *
from permissions import JustMe
from models import *
from datetime import datetime, timedelta, date, time
from utilities import *



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


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    #TODO: creators only can have permission to modify/make

class ArtistViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    


class EventListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventListSerializer

class FeaturedEventsList(EventListView):
    queryset = Event.objects.filter( is_featured=True )

class EventsNearYouList(EventListView):
    queryset = Event.objects.all() #TODO: geoDistance in python
    
class EventsForYouList(EventListView):
    def get_queryset(self):
        return self.request.user.fiprofile.autovocated_events()

class EventsHappeningNowList(EventListView):
    def get_queryset(self):
        hasnt_ended = Q( end__gt=localNow() )
        starts_by_tomorrow = Q( start__lt=endOfTomorrow() )
        return Event.objects.filter(
            hasnt_ended & starts_by_tomorrow
        ).order_by('end')





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
        'thetime': localNow(),
    })

def renderView( request, template, context={} ):
    injectDefaultContext( template, context )
    return render( request, template, context )

def renderPage( request, template, context={} ):
    return renderView( request, template+'.html', context )




def front(q):
    now = localNow().time()
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

    return renderPage(q, 'explore/events/'+view_type, {
        'list_name': list_name,
        'list_title': event_lists[list_name],
        'gmaps_api_key': settings.gmaps_api_key,
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
    if q.user.is_authenticated and q.user.fiprofile.isUnifithic():
        k = q.user.fiprofile.myFithing().pk
        yourProfileURL = 'profile/' + unicode(k) + '/'
    else:
        yourProfileURL = '#yo-dude-you-need-to-make-yo-first-fithing'
    return renderPage(q, 'create/create-home', {
        'yourProfileURL': yourProfileURL,
    })

def newThing(request, kindofthing):
    if kindofthing not in KindOfThings:
        raise Http404
    return renderPage(request, 'fithifile/fithifile', {
        'kindofthing': kindofthing,
        'isEditing': True,
    })

from djangular.forms.angular_model import NgModelFormMixin
from django.forms import ModelForm, TextInput, Textarea
TextFormControl = TextInput(attrs={'class':'form-control'})
TextareaFormControl = Textarea(attrs={'class': 'form-control'})
class FithingForm(NgModelFormMixin, ModelForm):
    form_name = 'fithiform' #note that these need to stay distinct
    scope_prefix = 'thing'
    class Meta:
        model = Fithing
        fields = ['name','logo','cover','brief','about',]
        widgets = {
            'name': TextFormControl,
            'brief': TextFormControl,
            'about': TextareaFormControl,
        }

#@login_required
def editThing(request, thingID):
    try:
        thing = Fithing.objects.get(pk=thingID)
        if thing.getManagers().filter(pk=request.user.pk).count() != 1:
            raise PermissionDenied
    except Fithing.DoesNotExist:
        raise Http404
    return renderPage(request, 'fithifile/fithifile', {
        'thing': thing,
        'kindofthing': thing.kindofthing(),
        'isEditing': True,
        'fithiform': FithingForm(),
    })
    
        


def connect(q):
    return renderPage(q, 'connect/connect-home')


def isUserFollowingThis(user, thingID):
    if not user.is_authenticated:
        return False
    qs = user.fiprofile.favorites.filter(pk=thingID)
    return qs.count() > 0

def profile(q, thingID):
    thing = Fithing.objects.get(pk=thingID)
    return renderPage(q, 'fithifile/fithifile', {
        'isEditing': False,
        'thing': thing,
        'kindofthing': thing.kindofthing,
        'isFollowingThis': isUserFollowingThis(q.user, thingID),
    })

def thing_events(q, thingID):
    return renderPage(q, 'profiles/thing-events', {
        'thing': Fithing.objects.get(pk=thingID),
    })

def alerts(q):
    return renderPage(q, 'alerts', {
        'alerts': ('stuff',)*482,
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

