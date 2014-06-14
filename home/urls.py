from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView

from home import views

urlpatterns = patterns(
    '',

    # Place the favicon in a standard static location but still conform to an old fashion favicon
#    url(r'^favicon\.ico$', RedirectView.as_view(url=s3+'main/icons/favicon.ico'), name='favicon'),

    url(r'^$', views.front, name='Front'),
    url(r'^$', views.front, name='Home'),

    url(r'^explore/$', views.explore, name='Explore'),
    url(r'^explore/featured/$', views.explore_featured, name='Featured'),
    url(r'^explore/featured/map/$', views.explore_map, name='Featured Map View'),
    url(r'^explore/near-you/$', views.explore_nearYou, name='Near You'),
    url(r'^explore/for-you/$', views.explore_forYou, name='For You'),
    url(r'^explore/fiddlr-events$', views.explore_fiddlrEvents, name='fiddlr Events'),
    url(r'^explore/happening-now/$', views.explore_happeningNow, name='Happening Now'),
    

    url(r'^create/', views.create, name='Create'),
    url(r'^connect/', views.connect, name='Connect'),


    url(r'^about/', views.about, name='About'),
    url(r'^about/', views.about, name='About Fiddlr'),
    url(r'^copyright/', views.copyrightView, name='Copyright'),
    url(r'^copyright/', views.copyrightView, name='Copyright Information'),
    url(r'^help/', views.helpView, name='Help'),
    url(r'^ads/', views.adsView, name='Ads'),
)
