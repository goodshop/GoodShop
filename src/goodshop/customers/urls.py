from django.conf.urls import patterns, include, url
from .views import CustomerRegistration

urlpatterns = patterns('',
    url(r'^((?P<context>(cat|search))/(?P<name>[-\w\s]+)/)?$', 'goodshop.customers.views.customer_home', name='customer_home'),
    url(r'^cart/$', 'goodshop.customers.views.shopping_cart', name='shopping_cart'),
    url(r'^cart/(?P<action>(add|remove|update|clear|checkout))/$', 'goodshop.customers.views.cart_manager', name='cart_manager'),
    url(r'^register/$', CustomerRegistration.as_view(), name='customer_registration'),
)