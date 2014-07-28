# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, Http404
from django.contrib import auth
from django.contrib.auth.views import login as auth_login_view
from django.contrib.auth.models import User as Djuser
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django import forms
from django.forms import ModelForm, ClearableFileInput
from djangular.forms.angular_model import NgModelFormMixin
from fiddlr import settings
from models import *
from utilities import *




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


def isSomeone(request, username):
    return (request.user.is_authenticated and
            request.user.username == username)

def isGabrielle(r):
    return isSomeone(r, 'gaby')
def isTheodore(r):
    return isSomeone(r, 'ted')


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
        'isTheodore': isTheodore(request),
        'useLESS': settings.TEMPLATE_DEBUG,
        'section': section,
        'page': page,
        'ngCDN': 'http://ajax.googleapis.com/ajax/libs/angularjs/',
        'ngVersion': '1.3.0-beta.13/',
        'thetime': localNow(),
        'CreotypeChoices': CreotypeChoices,
    })

    if 'ngScopeVars' in context:
        context['ngScopeInitials'] = {}
        for symbol in context['ngScopeVars']:
            if symbol in context:
                context['ngScopeInitials'].update({
                    symbol: context[symbol],
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



def signup(q):
    if q.method == 'POST':
        code = q.POST['accessCode']
        if code != 'musicologenealogipositorology':
            raise PermissionDenied
        uname = q.POST['username']
        email = q.POST['email']
        pword = q.POST['password']
        Djuser.objects.create_user(uname, email, pword)
        #TODO: handle failure to create user
        user = auth.authenticate(username=uname, password=pword)
        if user is not None and user.is_active:
            profile = Uzer(user=user)
            profile.save()
            auth.login(q, user)
            return HttpResponseRedirect('/account/')

    return HttpResponseRedirect(q.META.get('HTTP_REFERER'))




# @login_required
# def creoPage(request, creoId, editing, context={}):
#     if not Creo.objects.filter(pk=creoId).exists():
#         raise Http404

#     context.update({
#         'isEditing': editing,
#         'creoId': creoId,
#         'isFollowingThis': getUzer(request).isFollowing(creoId),
#         'ngScopeVars': ('isEditing', 'creoId'),
#     })
#     return renderPage(q, 'creo/creo-page', context)



#  _____  _____ ___ ___ ___ ___ _  _  ___ ___ 
# | __\ \/ / _ \ __| _ \_ _| __| \| |/ __| __|
# | _| >  <|  _/ _||   /| || _|| .` | (__| _| 
# |___/_/\_\_| |___|_|_\___|___|_|\_|\___|___|


@login_required
def experienceCreo(q, creoId):
    if not Creo.objects.filter(pk=creoId).exists():
        raise Http404

    return renderPage(q, 'creo/creo-page', {
        'isEditing': False,
        'creoId': creoId,
        'isFollowingThis': getUzer(q).isFollowing(creoId),
        'ngScopeVars': ('isEditing', 'creoId'),
    })



#TODO: don't make this a view, make an api point for creos' events
@login_required
def experienceCreoEvents(q, creoId):
    raise Http404 #Haven't made this template yet
    return renderPage(q, 'creo/creo-events', {
        'creo': get_object_or_404(Creo, pk=creoId),
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
def experienceEventListing(q, listingKey, viewType):
    if listingKey not in EventListings:
        raise Http404
    if viewType not in EventListingViewTypes:
        raise Http404

    return renderPage(q, 'experience/events/'+viewType, {
        'listingKey': listingKey,
        'listingTitle': EventListings[listingKey],
        'googleAPIKey': settings.googleAPIKey,
    })


@login_required
def experienceEventListingList(q, listingKey):
    return experienceEventListing(q, listingKey, 'list')

@login_required
def experienceEventListingMap(q, listingKey):
    return experienceEventListing(q, listingKey, 'map')




#   ___ ___ ___   _ _____ ___ 
#  / __| _ \ __| /_\_   _| __|
# | (__|   / _| / _ \| | | _| 
#  \___|_|_\___/_/ \_\_| |___|


@login_required
def createHome(q):
    if q.user.is_authenticated and getUzer(q).creos.count() > 0:
        k = getUzer(q).creos.all()[0].pk
        yourProfileURL = 'edit/%d/' % k
        #TODO: change for multicreo creators
    else:
        yourProfileURL = '#'
    return renderPage(q, 'create/create-home', {
        'yourProfileURL': yourProfileURL,
    })



def getOwnedCreo(request, creoId):
    creo = get_object_or_404(Creo, pk=creoId)
    if not creo.isEditor(getUzer(request).pk):
        raise PermissionDenied
    return creo

class PrettyNgModelFormMixin(NgModelFormMixin):
    def get_widget_attrs(self, bound_field):
        attrs = super(PrettyNgModelFormMixin, 
                      self).get_widget_attrs(bound_field)
        if attrs.has_key('class'):
            attrs['class'] += ' form-control '
        else:
            attrs.update({'class': 'form-control'})
        return attrs

def ngFileInput( fieldName ):
    return ClearableFileInput(attrs={
        'ng-file-select': "onFileChanged('%s', $files)" % fieldName
    })

class CreoForm(PrettyNgModelFormMixin, ModelForm):
    form_name = 'creoForm' #note that these need to stay distinct
    scope_prefix = 'creo'
    class Meta:
        model = Creo
        fields = ['name','logo','cover','brief','about','location']
        widgets = {
            'cover': ngFileInput('cover'),
            'logo': ngFileInput('logo'),
        }

@login_required
def editCreo(request, creoId):
    creo = getOwnedCreo(request, creoId)
    return renderPage(request, 'creo/creo-page', {
        'creoId': creoId,
        'creo': creo,
        'creotype': creo.creotype,
        'isEditing': True,
        'creoForm': CreoForm(),
        'ngScopeVars': ('isEditing', 'creoId'),
    })
    

@login_required
def newCreo(request, creotypeName):
    if creotypeName not in ValidCreotypeNames:
        raise Http404
    creo = Creo(creotype=creotypeForName(creotypeName))
    creo.save()
    creo.editors.add(getUzer(request))
    return editCreo(request, creo.pk)








@login_required
def alerts(q):
    return renderPage(q, 'alerts', {
        'alerts': ('stuff',)*482,
    })


#TODO: turn search results into an api outlet
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

        results = Creo.objects.filter(qWhere & qWhat)
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



































#    _____ ________________  ____________   _____   ____  _   ________
#   / ___// ____/ ____/ __ \/ ____/_  __/  /__  /  / __ \/ | / / ____/
#   \__ \/ __/ / /   / /_/ / __/   / /       / /  / / / /  |/ / __/   
#  ___/ / /___/ /___/ _, _/ /___  / /       / /__/ /_/ / /|  / /___   
# /____/_____/\____/_/ |_/_____/ /_/       /____/\____/_/ |_/_____/   


def LocusPropriusGabriellae(q):
    if not isGabrielle(q):
        raise PermissionDenied
    return renderPage(q, 'special/Locus-Proprius-Gabriellae')
