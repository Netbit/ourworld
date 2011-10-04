from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('mapapp.views',
    url(r'^$', 'home'),
    url(r'^lookup/$', 'lookup'),
    url(r'^info/(?P<id>\d+)/$', 'get_information'),
    url(r'^filter/district/$', 'district_filter'),
    url(r'^filter/kind_person/$', 'kind_person_filter'),
    url(r'^filter/kind_construction/$', 'kind_construction_filter'),
)
