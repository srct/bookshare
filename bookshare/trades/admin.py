from django.contrib import admin
from .models import Bid, Listing, Flag


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'bidder', 'listing',
                    'price', 'text')
    list_filter = ('created', 'modified', 'bidder', 'price')


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'title', 'author', 'isbn',
                    'year', 'edition', 'condition', 'description',
                    'price', 'sold', 'cancelled', 'winning_bid', 'date_closed')
    list_filter = ('created', 'modified', 'seller', 'condition',
                   'price', 'cancelled')

# expand this later
admin.site.register(Flag)
