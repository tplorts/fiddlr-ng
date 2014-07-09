from django.conf.urls import patterns, url, include
from django.views.generic.base import RedirectView
from django.contrib.auth.views import logout as auth_logout_view
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from home import views
from fiddlr import settings


router = routers.DefaultRouter( trailing_slash=False )
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'artists', views.ArtistViewSet)


urlpatterns = patterns(
    '',

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Place the favicon in a standard static location but still conform to an old fashion favicon
#    url(r'^favicon\.ico$', RedirectView.as_view(url=s3+'main/icons/favicon.ico'), name='favicon'),

    url(r'^$', views.front, name='Front'),
    url(r'^$', views.front, name='Home'),

    # REGISTRATION
    url(r'^login/$',  views.login, name='Login'),
    url(r'^logout/$', auth_logout_view, name='Logout'),
    url(r'^signup/$', views.signup, name='Signup'),
    url(r'^account/$', views.account, name='Account'),

    # EXPLORE
    url(r'^explore/$', views.explore, name='Explore'),
    url(r'^explore/events/(?P<list_name>[\w\d\-]+)/$', views.explore_events_list, name='Events List'),
    url(r'^explore/events/(?P<list_name>[\w\d\-]+)/map/$', views.explore_events_map, name='Events Map'),

    # EXPLORE PROFILE
    url(r'^explore/profile/$', views.explore_profile, name='Explore Profile'),
    url(r'^explore/profile/events$', views.explore_profile_events, name='Explore Favorite Events'),
    url(r'^explore/profile/artists$', views.explore_profile_artists, name='Explore Favorite Artists'),
    url(r'^explore/profile/venues$', views.explore_profile_venues, name='Explore Favorite Venues'),
    url(r'^explore/profile/for-me$', views.explore_profile_forMe, name='Explore For Me'),
    url(r'^explore/profile/near-me$', views.explore_profile_nearMe, name='Explore Near Me'),
    url(r'^explore/profile/browse$', views.explore_profile_browse, name='Explore Browse'),


    url(r'^create/$', views.create, name='Create'),
    url(r'^create/new-(\w+)/$', views.newThing),

    url(r'^connect/', views.connect, name='Connect'),


    url(r'^alerts/', views.alerts, name='Alerts'),

    url(r'^search/', views.search, name='Search'),

    url(r'^profile/(\d+)/$', views.profile, name='Profile'),
    url(r'^profile/(\d+)/events/$', views.thing_events),

    url(r'^about/', views.about, name='About'),
    url(r'^about/', views.about, name='About Fiddlr'),
    url(r'^copyright/', views.copyrightView, name='Copyright'),
    url(r'^copyright/', views.copyrightView, name='Copyright Information'),
    url(r'^help/', views.helpView, name='Help'),
    url(r'^ads/', views.adsView, name='Ads'),
)


urlpatterns += format_suffix_patterns(patterns(
    '',
    url(r'^custom-api/exists/user/(?P<username>[\w\d\-\.\+\@\_]{0,30})/$', views.UserExistsView.as_view()),
    url(r'^custom-api/set-password/$', views.SetPasswordView.as_view()),
    url(r'^custom-api/is-email-verified/$', views.IsEmailVerifiedView.as_view()),

    url(r'^custom-api/events/featured/$', views.FeaturedEventsList.as_view()),
    url(r'^custom-api/events/near-you/$', views.EventsNearYouList.as_view()),
    url(r'^custom-api/events/for-you/$', views.EventsForYouList.as_view()),
    url(r'^custom-api/events/happening-now/$', views.EventsHappeningNowList.as_view()),
))


if not settings.isProduction:
    urlpatterns += patterns(
        '',
        url(r'^404/$', views.test404),
        url(r'^500/$', views.test500),
    )
