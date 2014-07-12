# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
from django.shortcuts import get_object_or_404





#  ██████╗ ███████╗███╗   ██╗███████╗██████╗ ██╗ ██████╗
# ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██║██╔════╝
# ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝██║██║     
# ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██║██║     
# ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║╚██████╗
#  ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝ ╚═════╝

# http://brack3t.com/our-custom-mixins.html
class LoginRequiredMixin(object):
    """
    View mixin which verifies that the user has authenticated.

    NOTE:
        This should be the left-most mixin of a view.
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class FiddlrSearchForm( forms.Form ):
    what = forms.CharField()
    where = forms.CharField(required=False)


def isGabrielle(request):
    return (request.user.is_authenticated and
            request.user.username == 'gaby')


def injectDefaultContext(request, template, context):
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
        'isGabrielle': isGabrielle(request),
        'useLESS': settings.TEMPLATE_DEBUG,
        'section': section,
        'page': page,
        'ngCDN': 'http://ajax.googleapis.com/ajax/libs/angularjs/',
        'ngVersion': '1.3.0-beta.13/',
        'thetime': localNow(),
    })


class Fiew(TemplateView):
    template = 'pagebase'

    def get_context_data(self, **kwargs):
        context = super(Fiew, self).get_context_data(**kwargs)
        injectDefaultContext(self.request, self.template, context)
        return context

    def get_template_names(self):
        return [self.template + '.html']


class IntraFiew(LoginRequiredMixin, Fiew):
    pass


def getFuser(q):
    if q.user.is_authenticated:
        return Fuser.objects.get(user=q.user.pk)
    return None






def renderView( request, template, context={} ):
    injectDefaultContext( request, template, context )
    return render( request, template, context )

def renderPage( request, template, context={} ):
    return renderView( request, template+'.html', context )




def signin(q):
    context = {
        'inpirationalQuote': 'When your mind is full of indecision, try thinking with your heart.',
    }
    tname = 'registration/signin'
    injectDefaultContext(q, tname, context)
    return auth_login_view(q, tname+'.html', 
                           extra_context=context)


secret_agents = ('the1&onlyGABY', 'H@NN@H',)
def signup(q):
    if q.method == 'POST':
        said = q.POST['secret_agent_id']
        if said not in secret_agents:
            raise PermissionDenied
        uname = q.POST['username']
        email = q.POST['email']
        pword = q.POST['password']
        User.objects.create_user(uname, email, pword)
        #TODO: handle failure to create user
        user = auth.authenticate(username=uname, password=pword)
        if user is not None and user.is_active:
            profile = Fuser(user=user)
            profile.save()
            auth.login(q, user)
            return HttpResponseRedirect('/account/')

    return HttpResponseRedirect(q.META.get('HTTP_REFERER'))




# ███████╗██╗  ██╗██████╗ ██╗      ██████╗ ██████╗ ███████╗
# ██╔════╝╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██╔══██╗██╔════╝
# █████╗   ╚███╔╝ ██████╔╝██║     ██║   ██║██████╔╝█████╗  
# ██╔══╝   ██╔██╗ ██╔═══╝ ██║     ██║   ██║██╔══██╗██╔══╝  
# ███████╗██╔╝ ██╗██║     ███████╗╚██████╔╝██║  ██║███████╗
# ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝


@login_required
def exploreFing(q, fingId):
    try:
        fing = Fing.objects.get(pk=fingId)
    except Fing.DoesNotExist:
        raise Http404

    if not q.user.is_authenticated:
        following = False
    else:
        following = getFuser(q).isFollowing(fingId)

    return renderPage(q, 'fing', {
        'isEditing': False,
        'fing': fing,
        'fype': fing.fype,
        'isFollowingThis': following
    })


@login_required
def exploreFingEvents(q, fingId):
    raise Http404 #Haven't made this template yet
    return renderPage(q, 'fing/fing-events', {
        'fing': Fing.objects.get(pk=fingId),
    })


EventListings = {
    'featured': 'Featured Events',
    'for-you': 'Events For You',
    'near-you': 'Events Near You',
    'happening-now': 'Events Happening Now',
    'fiddlr-events': 'fiddlr events',
}
EventListingViewTypes = ('list', 'map')


@login_required
def exploreEventListing(q, listingKey, viewType):
    if listingKey not in EventListings:
        raise Http404
    if viewType not in EventListingViewTypes:
        raise Http404

    return renderPage(q, 'explore/events/'+viewType, {
        'listingKey': listingKey,
        'listingTitle': EventListings[listingKey],
        'gmapsAPIKey': settings.gmapsAPIKey,
    })


@login_required
def exploreEventListingList(q, listingKey):
    return exploreEventListing(q, listingKey, 'list')

@login_required
def exploreEventListingMap(q, listingKey):
    return exploreEventListing(q, listingKey, 'map')





#  ██████╗██████╗ ███████╗ █████╗ ████████╗███████╗
# ██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝
# ██║     ██████╔╝█████╗  ███████║   ██║   █████╗  
# ██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██╔══╝  
# ╚██████╗██║  ██║███████╗██║  ██║   ██║   ███████╗
#  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝

@login_required
def createHome(q):
    if q.user.is_authenticated and getFuser(q).fings.count() > 0:
        k = getFuser(q).fings.all()[0].pk
        yourProfileURL = 'profile/%d/' % k
        #TODO: change for multifing creators
    else:
        yourProfileURL = '#yo---you-should-like--create-somefing'
    return renderPage(q, 'create/create-home', {
        'yourProfileURL': yourProfileURL,
    })


@login_required
def newFing(request, fype):
    if fype not in ValidFypes:
        raise Http404
    return renderPage(request, 'fing/fing-page', {
        'fype': fype,
        'isEditing': True,
    })

from djangular.forms.angular_model import NgModelFormMixin
from django.forms import ModelForm, TextInput, Textarea
TextFormControl = TextInput(attrs={'class': 'form-control'})
TextareaFormControl = Textarea(attrs={'class': 'form-control'})
class FingForm(NgModelFormMixin, ModelForm):
    form_name = 'fingForm' #note that these need to stay distinct
    scope_prefix = 'fing'
    class Meta:
        model = Fing
        fields = ['name','logo','cover','brief','about',]
        widgets = {
            'name': TextFormControl,
            'brief': TextFormControl,
            'about': TextareaFormControl,
        }

@login_required
def editFing(request, fingId):
    try:
        fing = Fing.objects.get(pk=fingId)
        if not request.user.is_authenticated or not fing.isManager(getFuser(request)):
            raise PermissionDenied
    except Fing.DoesNotExist:
        raise Http404
    return renderPage(request, 'fing/fing-page', {
        'fingId': fingId,
        'fing': fing,
        'fype': fing.fype(),
        'isEditing': True,
        'fingForm': FingForm(),
    })
    
        



@login_required
def alerts(q):
    return renderPage(q, 'alerts', {
        'alerts': ('stuff',)*482,
    })


@login_required
def search(q):
    c = {}
    if q.method == 'POST':
        form = FiddlrSearchForm( q.POST )
        what = form.data['what']
        where = form.data['where']

        qWhat  = ( Q( name__icontains=what ) | 
                   Q( brief__icontains=what ) |
                   Q( about__icontains=what ) )

        qWhere = ( Q( location__address__icontains=where ) |
                   Q( location__neighborhood__icontains=where ) |
                   Q( location__zipcode=where ) )

        results = Fing.objects.filter(qWhere & qWhat)
        c.update({'searchResults': results})
    else:
        form = FiddlrSearchForm()
    c.update({'searchForm': form})
    return renderPage(q, 'search', c)





if not settings.isProduction:
    def test404(q):
        return render(q, '404.html', {})
    def test500(q):
        return render(q, '500.html', {})





#  █████╗ ██████╗ ██╗
# ██╔══██╗██╔══██╗██║
# ███████║██████╔╝██║
# ██╔══██║██╔═══╝ ██║
# ██║  ██║██║     ██║
# ╚═╝  ╚═╝╚═╝     ╚═╝

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
            isVerified = getFuser(request).isEmailVerified
        except Fuser.DoesNotExist:
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
    queryset = Fing.objects.filter(QEvent)
    serializer_class = FingSerializer
    #TODO: creators only can have permission to modify/make

class ArtistViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Fing.objects.filter(QArtist)
    serializer_class = FingSerializer
    


class EventListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventListSerializer

class FeaturedEventsList(EventListView):
    queryset = Fing.objects.filter(QEvent)
    #TODO: probably can't get away with not returning a queryset
    #      to feature objects instead of event objects

class EventsNearYouList(EventListView):
    queryset = Fing.objects.filter(QEvent) 
    #TODO: geoDistance in python
    
class EventsForYouList(EventListView):
    def get_queryset(self):
        return getFuser(self.request).autovocatedEvents()

class EventsHappeningNowList(EventListView):
    def get_queryset(self):
        hasntEnded = Q( end__gt=localNow() )
        startsByTomorrow = Q( start__lt=endOfTomorrow() )
        return Fing.objects.filter(
            QEvent &
            hasntEnded & startsByTomorrow
        ).order_by('end')





























#    _____ ________________  ____________   _____   ____  _   ________
#   / ___// ____/ ____/ __ \/ ____/_  __/  /__  /  / __ \/ | / / ____/
#   \__ \/ __/ / /   / /_/ / __/   / /       / /  / / / /  |/ / __/   
#  ___/ / /___/ /___/ _, _/ /___  / /       / /__/ /_/ / /|  / /___   
# /____/_____/\____/_/ |_/_____/ /_/       /____/\____/_/ |_/_____/   


def LocusPropriusGabriellae(q):
    if not isGabrielle(q):
        raise PermissionDenied
    return renderPage(q, 'special/Locus-Proprius-Gabriellae')
