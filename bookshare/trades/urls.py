# core django imports
from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page
# imports from your apps
from .views import ListListings, CreateListing, ListingPage,\
    CreateFlag, DeleteFlag, EditListing, ExchangeListing,\
    UnExchangeListing, CancelListing, ReopenListing, CreateRating,\
    EditRating, DeleteRating, EditBid, DeleteListing


urlpatterns = patterns('',
    url(r'^all/$',
        cache_page(60 * 2)(ListListings.as_view()), name='list_listings'),

    url(r'^new/$',
        CreateListing.as_view(), name='create_listing'),

    url(r'^listing/(?P<slug>[\w-]+)/$',
        cache_page(6)(ListingPage.as_view()), name='detail_listing'),

    url(r'^listing/(?P<slug>[\w-]+)/delete/$',
        DeleteListing.as_view(), name='delete_listing'),

    url(r'^listing/(?P<listing_slug>[\w-]+)/bid/(?P<slug>[\w-]+)/edit/$',
        EditBid.as_view(), name='edit_bid'),

    url(r'^listing/(?P<slug>[\w-]+)/flag/$',
        CreateFlag.as_view(), name='create_flag'),

    url(r'^listing/(?P<listing_slug>[\w-]+)/flag/(?P<slug>[\w-]+)/remove/$',
        DeleteFlag.as_view(), name='delete_flag'),

    url(r'^listing/(?P<slug>[\w-]+)/edit/$',
        EditListing.as_view(), name='edit_listing'),

    url(r'^listing/(?P<slug>[\w-]+)/exchange/$',
        ExchangeListing.as_view(), name='exchange_listing'),

    url(r'^listing/(?P<slug>[\w-]+)/unexchange/$',
        UnExchangeListing.as_view(), name='unexchange_listing'),

    url(r'^listing/(?P<slug>[\w-]+)/cancel/$',
        CancelListing.as_view(), name='cancel_listing'),

    url(r'^listing/(?P<slug>[\w-]+)/reopen/$',
        ReopenListing.as_view(), name='reopen_listing'),

    url(r'^listing/(?P<slug>[\w-]+)/rate/$',
        CreateRating.as_view(), name='create_rating'),

    url(r'^listing/(?P<listing_slug>[\w-]+)/rating/(?P<slug>[\w-]+)/edit/$',
        EditRating.as_view(), name='edit_rating'),

    url(r'^listing/(?P<listing_slug>[\w-]+)/rating/(?P<slug>[\w-]+)/remove/$',
        DeleteRating.as_view(), name='delete_rating'),

)
