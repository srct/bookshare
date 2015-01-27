from django.contrib import admin
from .models import Bid, Listing

# Register your models here.
@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
	list_display = ('id', 'created', 'modified', 'bidder', 'listing', 'price', 'text')
	list_filter = ('created', 'modified', 'bidder', 'price')

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
	list_display = ('id', 'created', 'modified', 'title', 'author', 'isbn', 'year', 'edition', 'date_sold', 'condition', \
	                'price', 'sold', 'active')
	list_filter = ('created', 'modified', 'seller', 'condition', 'price', 'active')
