from django.conf.urls import patterns, url, include
from django.views.generic.base import RedirectView
from django.contrib.auth.views import logout as auth_logout_view
from django.templatetags.static import static
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from home import views
from home.views import *
from fiddlr import settings


router = routers.DefaultRouter( trailing_slash=False )
# Not using trailing slashes on the API now because angular
# presently does not respect the trailing slash upon issuing
# API-bound requests.
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'creo', CreoViewSet)

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

    # EXPLORE
    url(r'^explore/$', IntraFiew.as_view(template='explore/explore-home'), name='Explore'),
    url(r'^explore/(\d+)/$', exploreCreo, name='Explore Creo'),
    url(r'^explore/(\d+)/events/$', exploreCreoEvents, name='Explore Creo Events'),
    url(r'^explore/events/([\w\d\-]+)/$', exploreEventListingList, name='Event Listing'),
    url(r'^explore/events/([\w\d\-]+)/map/$', exploreEventListingMap, name='Event Listing Map'),

    # EXPLORE PROFILE
    url(r'^explore/profile/$', IntraFiew.as_view(template='explore/profile/root'), name='Explore Profile'),
    url(r'^explore/profile/events$', IntraFiew.as_view(template='explore/profile/events'), name='Explore Favorite Events'),
    url(r'^explore/profile/artists$', IntraFiew.as_view(template='explore/profile/artists'), name='Explore Favorite Artists'),
    url(r'^explore/profile/venues$', IntraFiew.as_view(template='explore/profile/venues'), name='Explore Favorite Venues'),
    url(r'^explore/profile/for-me$', IntraFiew.as_view(template='explore/profile/for-me'), name='Explore For Me'),
    url(r'^explore/profile/near-me$', IntraFiew.as_view(template='explore/profile/near-me'), name='Explore Near Me'),
    url(r'^explore/profile/browse$', IntraFiew.as_view(template='explore/profile/browse'), name='Explore Browse'),


    url(r'^create/$', createHome, name='Create'),
    url(r'^create/new/', newCreo),
    url(r'^create/edit/(\d+)/$', editCreo),

    url(r'^connect/', IntraFiew.as_view(template='connect/connect-home'), name='Connect'),


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
