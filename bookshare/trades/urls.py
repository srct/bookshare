from django.conf.urls import patterns, include, url

from trades.views import ListListings, CreateListing, ListingPage, CreateFlag, DeleteFlag, EditListing, SellListing, UnSellListing, CancelListing, ReopenListing
from trades.models import Listing, Bid

urlpatterns = patterns('',

    url(r'^all/$',
        ListListings.as_view(
            model=Listing,
            paginate_by = 15,
            queryset=Listing.objects.exclude(cancelled=True).order_by('-created'),
            context_object_name='listings',
            template_name='list_listings.html'),
        name='list_listings'),

    url(r'^new/$',
        CreateListing.as_view(
            model=Listing,
            template_name='create_listing.html'),
        name='create_listing'),

    url(r'^listing/(?P<slug>[\w-]+)/$',
        ListingPage.as_view(),
        name='detail_listing'),

    url(r'^listing/(?P<slug>[\w-]+)/flag/$',
        CreateFlag.as_view(),
        name='create_flag'),

    url(r'^listing/(?P<listing_slug>[\w-]+)/flag/(?P<slug>[\w-]+)/remove/$',
        DeleteFlag.as_view(),
        name='delete_flag'),

    url(r'^listing/(?P<slug>[\w-]+)/edit/$',
        EditListing.as_view(
            model=Listing,
            template_name = 'listing_edit.html'),
        name='edit_listing'),

    url(r'^listing/(?P<slug>[\w-]+)/sell/$',
        SellListing.as_view(
            model=Listing,
            template_name = 'listing_sell.html'),
        name='sell_listing'),

    url(r'^listing/(?P<slug>[\w-]+)/unsell/$',
        UnSellListing.as_view(
            model=Listing,
            template_name = 'listing_unsell.html'),
        name='unsell_listing'),

    url(r'^listing/(?P<slug>[\w-]+)/cancel/$',
        CancelListing.as_view(
            model=Listing,
            template_name = 'listing_cancel.html'),
        name='cancel_listing'),

    url(r'^listing/(?P<slug>[\w-]+)/reopen/$',
        ReopenListing.as_view(
            model=Listing,
            template_name = 'listing_reopen.html'),
        name='reopen_listing'),
)
