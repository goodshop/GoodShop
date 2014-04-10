from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('signups.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about-us$', 'signups.views.aboutus', name='aboutus'),

    # including the register app urls
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^users/(?P<usr>[-\w]+)/$', 'signups.views.thankyou', name='thankyou'),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT
                          )
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT
                          )