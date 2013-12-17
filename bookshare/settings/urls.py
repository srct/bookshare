## DEVELOPMENT IMPORTS
from django.conf import settings
from django.conf.urls.static import static
## DEVELOPMENT IMPORTS

from django.contrib import admin
from django.contrib import auth
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

handle404 = "error_404"
handle500 = "error_500"

urlpatterns = patterns('website.views',
    # Examples:
    # url(r'^$', 'bookshare.views.home', name='home'),
    # url(r'^bookshare/', include('bookshare.foo.urls')),

    #### USER PAGES ####
    # home page
    url(r'^$', 'index', name = 'homepage'),
    # user profile page
    url(r'^u/(?P<username>\w+)/?$', 'profile', name = 'profile'),
    # book listing page
    url(r'^u/(?P<username>\w+)/listings/(?P<book_id>\w+)$', 'listing', name = 'listing'),
    # manage books you're looking for
    url(r'^u/(?P<username>\w+)/lookouts/$', 'lookouts', name = 'lookouts'),

    #### STATIC PAGES ####
    # about page
    url(r'^about/?$', 'about', name = 'about'),
    # contact staff
    url(r'^contact/?$', 'contact', name = 'contact'),
    # privacy policy
    url(r'^privacy/?$', 'privacy', name = 'privacy'),

    #### LISTING MANAGEMENT PAGES ####
    # create new listing
    url(r'^create/?$', 'create_listing', name = 'create_listing'),
    # search for listing
    url(r'^search/?$', 'search', name = 'search'),
    # close listing
    url(r'^close/(?P<book_id>\w+)$', 'close_listing', name='close_listing'),
    # sell listing
    url(r'^sell/(?P<book_id>\w+)$', 'sell_listing', name='sell_listing'),

    #### ADMIN PAGES ####
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #### COMMENTS APP ####
    (r'^comments/', include('django.contrib.comments.urls')),

)

urlpatterns += patterns('django.contrib.auth.views',                               
    #### AUTH PAGES ####                                                           
    url(r'^login$', 'login', {'template_name': 'login.html'},                      
        name='website_login'),                                                     
    url(r'^logout$', 'logout', {'next_page': '/'}, name='website_logout'),         
)
