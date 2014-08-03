from django.conf.urls import patterns, url, include
from django.views.generic.base import RedirectView
from django.contrib.auth.views import logout as auth_logout_view
from django.templatetags.static import static
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from home import views
from home.views import *
from home.api import *
from fiddlr import settings


router = routers.DefaultRouter()
#router.register(r'users', UserViewSet)
#router.register(r'groups', GroupViewSet)
router.register(r'creo', CreoViewSet)
router.register(r'location', LocationViewSet)


urlpatterns = patterns(
    '',

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Place the favicon in a standard static location but still conform to an old fashion favicon
    url(r'^favicon\.ico$', RedirectView.as_view(url=static('ex/icons/favicon.ico')), name='favicon'),

    url(r'^$', Fiew.as_view(template='front'), name='Home'),

    # REGISTRATION
    url(r'^signin/$', signin, name='Sign in'),
    url(r'^signup/$', signup, name='Sign up'),
    url(r'^signout/$', auth_logout_view, name='Sign out'),
    url(r'^account/$', IntraFiew.as_view(template='registration/account'), name='Account'),

    # EXPERIENCE
    url(r'^experience/$', IntraFiew.as_view(template='experience/experience-home'), name='Experience'),
    url(r'^experience/(\d+)/$', experienceCreo, name='Experience Creo'),
    url(r'^experience/(\d+)/events/$', experienceCreoEvents, name='Experience Creo Events'),
    url(r'^experience/events/([\w\d\-]+)/$', experienceEventListingList, name='Event Listing'),
    url(r'^experience/events/([\w\d\-]+)/map/$', experienceEventListingMap, name='Event Listing Map'),

    # EXPERIENCE PROFILE
    url(r'^experience/profile/$', IntraFiew.as_view(template='experience/profile/root'), name='Experience Profile'),
    url(r'^experience/profile/events$', IntraFiew.as_view(template='experience/profile/events'), name='Experience Favorite Events'),
    url(r'^experience/profile/artists$', IntraFiew.as_view(template='experience/profile/artists'), name='Experience Favorite Artists'),
    url(r'^experience/profile/venues$', IntraFiew.as_view(template='experience/profile/venues'), name='Experience Favorite Venues'),
    url(r'^experience/profile/for-me$', IntraFiew.as_view(template='experience/profile/for-me'), name='Experience For Me'),
    url(r'^experience/profile/near-me$', IntraFiew.as_view(template='experience/profile/near-me'), name='Experience Near Me'),
    url(r'^experience/profile/browse$', IntraFiew.as_view(template='experience/profile/browse'), name='Experience Browse'),


    url(r'^create/$', createHome, name='Create'),
    url(r'^create/new/(\w+)/$', newCreo, name='new-creo'),
    url(r'^create/edit/(\d+)/$', editCreo, name='edit-creo'),

    url(r'^nexus/', IntraFiew.as_view(template='nexus/nexus-home'), name='Nexus'),


    url(r'^alerts/', alerts, name='Alerts'),

    url(r'^search/', search, name='Search'),

    url(r'^about/', Fiew.as_view(template='auxiliary/about'), name='About'),
    url(r'^copyright/', Fiew.as_view(template='auxiliary/copyright'), name='Copyright'),
    url(r'^help/', Fiew.as_view(template='auxiliary/help'), name='Help'),
    url(r'^ads/', Fiew.as_view(template='auxiliary/ads'), name='Ads'),
)


urlpatterns += format_suffix_patterns(patterns(
    '',
    url(r'^custom-api/exists/user/(?P<username>[\w\d\-\.\+\@\_]{0,30})/$', UserExistsView.as_view()),
    url(r'^custom-api/set-password/$', SetPasswordView.as_view()),
    url(r'^custom-api/is-email-verified/$', IsEmailVerifiedView.as_view()),

#    url(r'^custom-api/creo/(\d+)/picture/$', uploadCreoPicture),

    url(r'^custom-api/events/featured/$', FeaturedEventsList.as_view()),
    url(r'^custom-api/events/near-you/$', EventsNearYouList.as_view()),
    url(r'^custom-api/events/for-you/$', EventsForYouList.as_view()),
    url(r'^custom-api/events/happening-now/$', EventsHappeningNowList.as_view()),
))


if not settings.isProduction:
    urlpatterns += patterns(
        '',
        url(r'^404/$', test404),
        url(r'^500/$', test500),
    )









































#    _____ ________________  ____________   _____   ____  _   ________
#   / ___// ____/ ____/ __ \/ ____/_  __/  /__  /  / __ \/ | / / ____/
#   \__ \/ __/ / /   / /_/ / __/   / /       / /  / / / /  |/ / __/   
#  ___/ / /___/ /___/ _, _/ /___  / /       / /__/ /_/ / /|  / /___   
# /____/_____/\____/_/ |_/_____/ /_/       /____/\____/_/ |_/_____/   


urlpatterns += patterns(
    '',
    url(r'^Locus-Proprius-Gabriellae/$', LocusPropriusGabriellae),
)
