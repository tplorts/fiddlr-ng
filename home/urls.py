from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView

from home import views

urlpatterns = patterns(
    '',

    # Place the favicon in a standard static location but still conform to an old fashion favicon
#    url(r'^favicon\.ico$', RedirectView.as_view(url=s3+'main/icons/favicon.ico'), name='favicon'),

    url(r'^$', views.front, name='Front'),
    url(r'^$', views.front, name='Home'),

    url(r'^explore/', views.explore, name='Explore'),
    url(r'^create/', views.create, name='Create'),
    url(r'^connect/', views.connect, name='Connect'),

    url(r'^about/', views.about, name='About'),
    url(r'^about/', views.about, name='About Fiddlr'),
    url(r'^copyright/', views.copyrightView, name='Copyright'),
    url(r'^copyright/', views.copyrightView, name='Copyright Information'),
    url(r'^help/', views.helpView, name='Help'),
    url(r'^ads/', views.adsView, name='Ads'),
)
