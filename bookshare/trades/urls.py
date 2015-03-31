from django.conf.urls import patterns, include, url

from trades.views import ListListings, CreateListing, ListingPage, UpdateListing, CloseListing
from trades.models import Listing

urlpatterns = patterns('',

    url(r'^all/$',
        ListListings.as_view(
            model=Listing,
            paginate_by = 15,
            queryset=Listing.objects.all().order_by('-created'),
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

    url(r'^listing/(?P<slug>[\w-]+)/update/$',
        UpdateListing.as_view(
            model=Listing,
            template_name = 'listing_update.html'),
        name='update_listing'),

    url(r'^listing/(?P<slug>[\w-]+)/close/$',
        CloseListing.as_view(
            model=Listing,
            template_name = 'listing_close.html'),
        name='close_listing'),
)
