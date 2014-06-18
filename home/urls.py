from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView

from home import views

urlpatterns = patterns(
    '',

    # Place the favicon in a standard static location but still conform to an old fashion favicon
#    url(r'^favicon\.ico$', RedirectView.as_view(url=s3+'main/icons/favicon.ico'), name='favicon'),

    url(r'^$', views.front, name='Front'),
    url(r'^$', views.front, name='Home'),

    # EXPLORE
    url(r'^explore/$', views.explore, name='Explore'),
    url(r'^explore/featured/$', views.explore_featured, name='Featured'),
    url(r'^explore/featured/map/$', views.explore_map, name='Featured Map View'),
    url(r'^explore/near-you/$', views.explore_nearYou, name='Near You'),
    url(r'^explore/for-you/$', views.explore_forYou, name='For You'),
    url(r'^explore/fiddlr-events$', views.explore_fiddlrEvents, name='fiddlr Events'),
    url(r'^explore/happening-now/$', views.explore_happeningNow, name='Happening Now'),

    # EXPLORE PROFILE
    url(r'^explore/profile/$', views.explore_profile, name='Explore Profile'),
    url(r'^explore/profile/events$', views.explore_profile_events, name='Explore Favorite Events'),
    url(r'^explore/profile/artists$', views.explore_profile_artists, name='Explore Favorite Artists'),
    url(r'^explore/profile/venues$', views.explore_profile_venues, name='Explore Favorite Venues'),
    url(r'^explore/profile/for-me$', views.explore_profile_forMe, name='Explore For Me'),
    url(r'^explore/profile/near-me$', views.explore_profile_nearMe, name='Explore Near Me'),
    url(r'^explore/profile/browse$', views.explore_profile_browse, name='Explore Browse'),


    url(r'^create/', views.create, name='Create'),
    url(r'^connect/', views.connect, name='Connect'),


    url(r'^artist/(\d+)/$', views.artist_page, name='Artist Page'),
    url(r'^event/(\d+)/$', views.event_page, name='Event Page'),
    url(r'^venue/(\d+)/$', views.venue_page, name='Venue Page'),
    

    url(r'^about/', views.about, name='About'),
    url(r'^about/', views.about, name='About Fiddlr'),
    url(r'^copyright/', views.copyrightView, name='Copyright'),
    url(r'^copyright/', views.copyrightView, name='Copyright Information'),
    url(r'^help/', views.helpView, name='Help'),
    url(r'^ads/', views.adsView, name='Ads'),
)
