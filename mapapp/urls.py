from django.conf.urls import patterns, url

urlpatterns = patterns('mapapp.views',
    url(r'^$', 'home'),
    url(r'^lookup/$', 'lookup'),
    url(r'^info/(?P<id_object>\d+)/$', 'place_info', name='place_info'),
    url(r'^details/(?P<id_object>\d+)/$', 'get_details', name="place_detail"),
    url(r'^search/$', 'search_place', name='search_place'),
    url(r'^filter/district/$', 'district_filter'),
    url(r'^filter/kind_person/$', 'kind_person_filter'),
    url(r'^filter/kind_construction/$', 'kind_construction_filter'),
    url(r'^get/person_construction/$', 'get_kind_person_contruction'),
    url(r'^admin/mapapp/construction/upload/$', 'upload_file'),
)
