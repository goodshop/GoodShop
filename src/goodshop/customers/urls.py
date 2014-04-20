from django.conf.urls import patterns, include, url
from .views import CustomerRegistration

urlpatterns = patterns('',
    url(r'^((?P<context>[-\w]+)/(?P<name>[-\w]+)/)?$', 'goodshop.customers.views.customer_home', name='customer_home'),
    url(r'^register/$', CustomerRegistration.as_view(), name='customer_registration'),
)