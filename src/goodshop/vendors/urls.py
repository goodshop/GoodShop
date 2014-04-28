from django.conf.urls import patterns, include, url
from .views import VendorRegistration

urlpatterns = patterns('',
    url(r'^$', 'goodshop.vendors.views.vendor_home', name='vendor_home'),
    url(r'^orders/$', 'goodshop.vendors.views.vendor_orders', name='vendor_orders'),
    url(r'^orders/(?P<order_id>[\d]+)/$', 'goodshop.vendors.views.vendor_order', name='vendor_order'),
    url(r'^my-products/$', 'goodshop.vendors.views.my_products', name='my_products'),
    url(r'^register/$', VendorRegistration.as_view(), name='vendor_registration'),
)