# standard library imports
from __future__ import absolute_import, print_function, unicode_literals
# third party imports
from rest_framework import serializers
# imports from your apps
from trades.models import Listing


class ListingSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name = 'detail_listing',
        lookup_field = 'slug'
    )

    class Meta:
        model = Listing
        fields = ('url', 'title', 'author', 'isbn', 'year', 'edition',
                  'condition', 'access_code', 'course_abbr', 'description',
                  'price', 'photo', 'exchanged', 'cancelled', 'exchanged')
