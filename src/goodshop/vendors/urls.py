from django.conf.urls import patterns, include, url
from .views import VendorRegistration

urlpatterns = patterns('',
    url(r'^$', 'goodshop.vendors.views.vendor_home', name='vendor_home'),
    url(r'^register/$', VendorRegistration.as_view(), name='vendor_registration'),
)