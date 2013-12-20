## DEVELOPMENT IMPORTS
from django.conf import settings
from django.conf.urls.static import static
## DEVELOPMENT IMPORTS

from django.contrib import admin
from django.contrib import auth
from django.conf.urls import patterns, include, url
from website.forms import StyledSearchForm
from haystack.views import SearchView

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

handle404 = "error_404"
handle500 = "error_500"

urlpatterns = patterns('website.views',
    #### USER PAGES ####
    # home page
    url(r'^$', 'index', name = 'homepage'),
    # user profile page
    url(r'^u/(?P<username>\w+)/?$', 'profile', name = 'profile'),
    # create lookout
    url(r'^u/(?P<username>\w+)/create-lookout/?$', 'create_lookout', name = 'create_lookout'),

    #### LISTING PAGES ####
    # global new listings page
    url(r'^listings/?$', 'all_listings', name = 'all_listings'),
    # create new listing
    url(r'^listings/create/?$', 'create_listing', name = 'create_listing'),
    # book listing page
    url(r'^listings/(?P<book_id>\d+)$', 'view_listing', name = 'view_listing'),

    #### STATIC PAGES ####
    # about page
    url(r'^about/?$', 'about', name = 'about'),
    # contact staff
    url(r'^contact/?$', 'contact', name = 'contact'),
    # privacy policy
    url(r'^privacy/?$', 'privacy', name = 'privacy'),
    # privacy opt-out (for piwik)
    url(r'^privacy/opt-out/?$', 'privacy_opt_out', name='privacy_opt_out'),

    #### SEARCH PAGES ####
    # points to a SearchView Instance
    #url(r'^search/', include('haystack.urls')),
    url(
        r'^search/?',
        SearchView(
            form_class = StyledSearchForm,
            results_per_page = 20,
        ),
        name = 'haystack_search',
    ),

    #### ADMIN PAGES ####
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

)

urlpatterns += patterns('django.contrib.auth.views',
    #### AUTH PAGES ####
    url(r'^login$', 'login', {'template_name': 'login.html'},
        name='website_login'),
    url(r'^logout$', 'logout', {'next_page': '/'}, name='website_logout'),
)
