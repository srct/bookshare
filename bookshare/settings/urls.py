from django.contrib import admin
from django.contrib import auth
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('website.views',
    # Examples:
    # url(r'^$', 'bookshare.views.home', name='home'),
    # url(r'^bookshare/', include('bookshare.foo.urls')),

    # home page
    url(r'^$', 'index', name = 'homepage'),

    # user profile page
    url(r'^u/(?P<slug>\w+)/?$', 'profile', name = 'profile'),

    # user listings page
    url(r'^u/(?P<slug>\w+)/listings/?$', 'user_listings', name = 'user_listings'),

    # book listing page
    url(r'^u/(?P<slug>\w+)/listings/(?P<book_slug>\w+)$', 'listing', name = 'listing'),

#    # create new listing
#    url(r'^create$', 'create_listing', name = 'new-listing'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
