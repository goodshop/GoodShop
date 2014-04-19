from django.conf.urls import patterns, include, url
from .views import CustomerRegistration, VendorRegistration

urlpatterns = patterns('',
    url(r'^$', 'django.contrib.auth.views.login', {'template_name':'inicio/index.html'}, name='login'),
    url(r'^home/$', 'signups.views.home', name='home'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^about-us/$', 'signups.views.aboutus', name='aboutus'),
    url(r'^thank-you/$', 'signups.views.thankyou', name='thankyou'),

    url(r'^customer/register/$', CustomerRegistration.as_view(), name='customer_registration'),
    url(r'^vendor/register/$', VendorRegistration.as_view(), name='vendor_registration'),
)