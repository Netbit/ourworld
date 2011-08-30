from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('mapapp.views',

    url(r'^$', 'home'),
    url(r'^lookup/$', 'lookup'),
)
