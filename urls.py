from django.conf.urls.defaults import patterns, include, url
import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
   
    url(r'^', include('mapapp.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)
