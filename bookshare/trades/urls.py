# core django imports
from django.urls import path
from django.views.decorators.cache import cache_page
# imports from your apps
from .views import ListListings, CreateListing, ListingPage,\
    CreateFlag, DeleteFlag, CreateBidFlag, DeleteBidFlag,\
    EditListing, ExchangeListing, UnExchangeListing, CancelListing,\
    ReopenListing, CreateRating, EditRating, DeleteRating,\
    EditBid, DeleteListing


urlpatterns = [
    path('all/',
        cache_page(60 * 2)(ListListings.as_view()), name='list_listings'),

    path('new/',
        CreateListing.as_view(), name='create_listing'),

    path('listing/<slug>/',
         cache_page(4)(ListingPage.as_view()), name='detail_listing'),

    path('listing/<slug>/delete/',
        DeleteListing.as_view(), name='delete_listing'),

    path('listing/<listing_slug>/bid/<slug>/edit/',
        EditBid.as_view(), name='edit_bid'),

    path('listing/<slug>/flag/',
        CreateFlag.as_view(), name='create_flag'),

    path('listing/<listing_slug>/flag/<slug>/remove/',
        DeleteFlag.as_view(), name='delete_flag'),

    path('listing/<listing_slug>/bid/<slug>/flag/',
        CreateBidFlag.as_view(), name='create_bid_flag'),

    path('listing/<listing_slug>/bid/<bid_slug>/flag/<slug>/remove/',
        DeleteBidFlag.as_view(), name='delete_bid_flag'),

    path('listing/<slug>/edit/',
        EditListing.as_view(), name='edit_listing'),

    path('listing/<slug>/exchange/',
        ExchangeListing.as_view(), name='exchange_listing'),

    path('listing/<slug>/unexchange/',
        UnExchangeListing.as_view(), name='unexchange_listing'),

    path('listing/<slug>/cancel/',
        CancelListing.as_view(), name='cancel_listing'),

    path('listing/<slug>/reopen/',
        ReopenListing.as_view(), name='reopen_listing'),

    path('listing/<slug>/rate/',
        CreateRating.as_view(), name='create_rating'),

    path('listing/<listing_slug>/rating/<slug>/edit/',
        EditRating.as_view(), name='edit_rating'),

    path('listing/<listing_slug>/rating/<slug>/remove/',
        DeleteRating.as_view(), name='delete_rating'),

]
