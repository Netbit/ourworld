from django.conf.urls import patterns, include, url
import settings

from django.contrib import admin

admin.autodiscover()

js_info_dict = {
    'packages': ('mapapp',),
}

urlpatterns = patterns('',

    url(r'^', include('mapapp.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
)
