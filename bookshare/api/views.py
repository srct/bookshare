# standard library imports
from __future__ import absolute_import, print_function
# third party imports
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ReadOnlyModelViewSet
# imports from your apps
from trades.models import Listing
from .serializers import ListingSerializer


# trades apis
class ListingPagination(PageNumberPagination):
    page_size = 100  # number of results per page
    page_size_query_param = 'page_size'
    max_page_size = 1000  # so you can retrieve a maximum of 100,000 listings


class ListingViewSet(ReadOnlyModelViewSet):
    queryset = Listing.objects.all().order_by('-created')
    serializer_class = ListingSerializer
    pagination_class = ListingPagination
    lookup_field = 'slug'
