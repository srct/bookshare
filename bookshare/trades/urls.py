from django.conf.urls import patterns, include, url

from trades.views import ListListings, CreateListing, DetailListing
from trades.models import Listing

urlpatterns = patterns('',

    url(r'^all/$',
        ListListings.as_view(
            model=Listing,
            paginate_by = 15,
            queryset=Listing.objects.all().order_by('-created'),
            context_object_name='listings',
            template_name='listListings.html'),
        name='all_listings'),

    url(r'^new/$',
        CreateListing.as_view(
            model=Listing,
            template_name='createListing.html'),
        name='createListing'),

    url(r'^(?P<slug>[\w-]+)/$',
        DetailListing.as_view(
            model=Listing,
            # slug_field='slug__exact',
            context_object_name='listing',
            template_name='listing.html'),
        name='listing'),

)
