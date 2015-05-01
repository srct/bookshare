# core django imports
from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page
# imports from your apps
from .views import ModLandingView, FlagModView, ListingNumModView,\
    UserEmailRatioModView

urlpatterns = patterns('',
    url(r'^$', cache_page(60 * 15)(ModLandingView.as_view()), name='mod_page'),

    url(r'^flags/$', FlagModView.as_view(), name='flag_mod'),

    url(r'^listing-nums/$', ListingNumModView.as_view(), name='listing_nums'),

    url(r'^email-ratio/$', UserEmailRatioModView.as_view(), name='email_ratio'),

)
