from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'goodshop.views.home', name='home'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name':'inicio/index.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    (r'^customer/', include('goodshop.customers.urls')),
    (r'^vendor/', include('goodshop.vendors.urls')),

    url(r'^about-us/$', 'goodshop.views.aboutus', name='aboutus'),
    url(r'^thank-you/$', 'goodshop.views.thankyou', name='thankyou'),
)