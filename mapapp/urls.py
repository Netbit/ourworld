from django.conf.urls.defaults import patterns, url
from django.views.decorators.cache import cache_page
from mapapp.views import get_details

urlpatterns = patterns('mapapp.views',
    url(r'^$', 'home'),
    url(r'^lookup/$', 'lookup'),
    url(r'^info/(?P<id_object>\d+)/$', 'get_information'),
    url(r'^details/(?P<id_object>\d+)/$', cache_page(get_details, 60*15)),
    url(r'^filter/district/$', 'district_filter'),
    url(r'^filter/kind_person/$', 'kind_person_filter'),
    url(r'^filter/kind_construction/$', 'kind_construction_filter'),
    url(r'^get/person_construction/$', 'get_kind_person_contruction'),
    url(r'^admin/mapapp/construction/upload/$', 'upload_file'),
)
