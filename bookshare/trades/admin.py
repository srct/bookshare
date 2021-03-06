# core django imports
from django.contrib import admin
# imports from your apps
from .models import Bid, Listing, Flag, BidFlag, Rating


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'bidder', 'listing',
                    'price', 'text')
    list_filter = ('created', 'modified', 'bidder', 'price')


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'title', 'author', 'isbn',
                    'year', 'edition', 'condition', 'description',
                    'price', 'exchanged', 'cancelled', 'winning_bid',
                    'date_closed')
    list_filter = ('created', 'modified', 'poster', 'condition',
                   'price', 'cancelled')

# expand this later
admin.site.register(Flag)
admin.site.register(BidFlag)
admin.site.register(Rating)
