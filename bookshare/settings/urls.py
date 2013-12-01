## DEVELOPMENT IMPORTS
from django.conf import settings
from django.conf.urls.static import static
## DEVELOPMENT IMPORTS

from django.contrib import admin
from django.contrib import auth
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

urlpatterns = patterns('website.views',
    # Examples:
    # url(r'^$', 'bookshare.views.home', name='home'),
    # url(r'^bookshare/', include('bookshare.foo.urls')),

    #### USER PAGES ####
    # user profile page
    url(r'^u/(?P<slug>\w+)/?$', 'profile', name = 'profile'),
    # user listings page
    url(r'^u/(?P<slug>\w+)/listings/?$', 'user_listings', name = 'user_listings'),
    # book listing page
    url(r'^u/(?P<slug>\w+)/listings/(?P<book_slug>\w+)$', 'listing', name = 'listing'),

    #### META PAGES ####
    # home page
    url(r'^$', 'index', name = 'homepage'),
    # about page
    url(r'^about/?$', 'about', name = 'about'),
    # contact staff
    url(r'^contact/?$', 'contact', name = 'contact'),
    # privacy policy
    url(r'^privacy/?$', 'privacy', name = 'privacy'),
#    # security policy
#    url(r'^security/?$', 'security', name = 'security'),

    #### LISTING MANAGEMENT PAGES ####
    # create new listing
    url(r'^create/?$', 'create_listing', name = 'create_listing'),
    # search for listing
    url(r'^search/?$', 'search', name = 'search'),

    #### ADMIN PAGES ####
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
