from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView

from home import views

urlpatterns = patterns(
    '',

    # Place the favicon in a standard static location but still conform to an old fashion favicon
#    url(r'^favicon\.ico$', RedirectView.as_view(url=s3+'main/icons/favicon.ico'), name='favicon'),

    url(r'^$', views.front, name='front'),

    url(r'^explore/', views.explore, name='explore'),
    url(r'^create/', views.create, name='create'),
    url(r'^connect/', views.connect, name='connect'),

    url(r'^about/', views.about, name='About Fiddlr'),
    url(r'^copyright/', views.copyrightView, name='Copyright Information'),
    url(r'^help/', views.helpView, name='Help'),
)
