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

    active = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    old = serializers.SerializerMethodField()
    num_bids = serializers.SerializerMethodField()
    num_flags = serializers.SerializerMethodField()

    def get_active(self, listing):
        return listing.active()

    def get_final_price(self, listing):
        return listing.final_price()

    def get_old(self, listing):
        return listing.old()

    def get_num_bids(self, listing):
        return listing.bid_set.all().count()

    def get_num_flags(self, listing):
        return listing.flag_set.all().count()

    class Meta:
        model = Listing
        fields = ('url', 'title', 'author', 'isbn', 'year', 'edition', 'condition',
                  'access_code', 'course_abbr', 'description', 'price', 'photo',
                  'num_bids', 'num_flags', 'active', 'old',
                  'exchanged', 'cancelled', 'date_closed', 'final_price')
