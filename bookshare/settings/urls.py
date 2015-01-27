from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin

# FIX SEARCH #
#from core.forms import StyledSearchForm
from haystack.views import SearchView

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

handle404 = TemplateView.as_view(template_name="404.html")
handle500 = TemplateView.as_view(template_name="500.html")

urlpatterns = patterns('',

    # app-level urls
    url(r'^share/', include('trades.urls')),
    # student urls?

    #### USER PAGES ####
    # home page
    url(r'^$', TemplateView.as_view(template_name='index.html'), name = 'homepage'),
    # user profile page
    url(r'^u/(?P<username>\w+)/?$', 'core.views.profile', name = 'profile'),
    # create lookout
    url(r'^u/(?P<username>\w+)/create-lookout/?$', 'lookouts.views.create_lookout', name = 'create_lookout'),

    #### LISTING PAGES ####
    # book listing page
    url(r'^listings/(?P<book_id>\d+)$', 'trades.views.view_listing', name = 'view_listing'),

    #### STATIC PAGES ####
    # about page
    url(r'^about/?$', TemplateView.as_view(template_name='about.html'), name='about'),
    # privacy policy
    url(r'^privacy/?$', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    # privacy opt-out (for piwik)
    url(r'^privacy/opt-out/?$', 'core.views.privacy_opt_out', name='privacy_opt_out'),

    #### SEARCH PAGES ####
    # points to a SearchView Instance
    #url(r'^search/', include('haystack.urls')),
    #url(
    #    r'^search/?',
    #    SearchView(
    #        form_class = StyledSearchForm,
    #        results_per_page = 20,
    #    ),
    #    name = 'haystack_search',
    #),

    url(r'^login/$', 'cas.views.login', name='login'),
    url(r'^logout/$', 'cas.views.logout', name='logout'),

    #### ADMIN PAGES ####
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

)
