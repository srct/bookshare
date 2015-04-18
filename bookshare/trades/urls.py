from django.conf.urls import patterns, url

from trades.views import ListListings, CreateListing, ListingPage,\
    CreateFlag, DeleteFlag, EditListing, SellListing,\
    UnSellListing, CancelListing, ReopenListing, CreateRating,\
    EditRating, DeleteRating


urlpatterns = patterns('',
    url(r'^all/$',
        ListListings.as_view(), name='list_listings'),

    url(r'^new/$',
        CreateListing.as_view(), name='create_listing'),

    url(r'^listing/(?P<slug>[\w-]+)/$',
        ListingPage.as_view(), name='detail_listing'),

    url(r'^listing/(?P<slug>[\w-]+)/flag/$',
        CreateFlag.as_view(), name='create_flag'),

    url(r'^listing/(?P<listing_slug>[\w-]+)/flag/(?P<slug>[\w-]+)/remove/$',
        DeleteFlag.as_view(), name='delete_flag'),

    url(r'^listing/(?P<slug>[\w-]+)/edit/$',
        EditListing.as_view(), name='edit_listing'),

    url(r'^listing/(?P<slug>[\w-]+)/sell/$',
        SellListing.as_view(), name='sell_listing'),

    url(r'^listing/(?P<slug>[\w-]+)/unsell/$',
        UnSellListing.as_view(), name='unsell_listing'),

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
