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

    active = serializers.SerializerMethodField('active')
    active = serializers.SerializerMethodField('final_price')
    active = serializers.SerializerMethodField('old')

    def active(self, listing):
        return listing.active()

    def final_price(self, listing):
        return listing.final_price()

    def old(self, listing):
        return listing.old()

    class Meta:
        model = Listing
        fields = ('url', 'title', 'author', 'isbn', 'year', 'edition', 'condition',
                  'access_code', 'course_abbr', 'description', 'price', 'photo',
                  'active', 'old',
                  'exchanged', 'cancelled', 'date_closed', 'final_price')
