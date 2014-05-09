from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import home
from home import urls


urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(home.urls)),
)
