from django.conf.urls.defaults import patterns, include, url
import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('mapapp.views',
   
    url(r'^$', 'home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)
