from django.conf.urls import patterns, include, url

from trades.views import ListListings, CreateListing
from trades.models import Listing

urlpatterns = patterns('',

    url(r'^all/$',
        ListListings.as_view(
            model=Listing,
            paginate_by = 25
            queryset=Listing.objects.all().order_by('-created')
            context_object_name='listings',
            template_name='listListings.html'),
        name='all_listings'),

    url(r'^new/$',
        CreateListing.as_view(
            model=Listing,
            template_name='createListing.html'),
        name='createListing'),
)
