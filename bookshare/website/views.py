from website.models import Listing,Seller
from website.forms import ListingForm, FinalPriceForm
from bids.models import Bid
from bids.forms import BidForm
from lookouts.models import Lookout
from django.http import Http404
from django.conf import settings
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.utils import timezone
from datetime import datetime,timedelta
from django.contrib.auth.decorators import login_required

import pyisbn
import requests

# pulls worldcat metadata from ISBNs
def ISBNMetadata(standardISBN):
    url = "http://xisbn.worldcat.org/webservices/xid/isbn/" + standardISBN + "?method=getMetadata&format=json&fl=title,year,author,ed"
    metadata = request.get(url)
    # format into a dictionary
    dejson = metadata.json()
    metadataDict = dejson['list'][0]
    return metadataDict

# gamification
def totalSold(seller):
    soldList = Listing.objects.filter(seller__user__username=seller)
    totalSold = 0
    for book in soldList:
        if book.sold and book.finalPrice:
            totalSold += book.finalPrice
    return totalSold

# validation of new listing forms
    # <3 test cases

# relevant comments
def relevantComments(seller):
    sellerListings = Listing.objects.filter(seller__user__username=seller).order_by("-date_created")
    # all listings that seller has commented on (preferably ordered in reverse)
    # put those lists together
    # return that list
    return False

# saved searches
    # need to implement haystack stuff first

# seller's rating
def ratingsAverage(seller):
    sellerRating = Seller.objects.filter(user__username=seller)
    ratingNumber = 0
    ratingTotal = 0
    ratingAverage = 0
    for rating in sellerRating:
        ratingNumber += 1
        ratingTotal += rating
    ratingAverage = ratingTotal/ratingNumber
    return ratingNumber


############# VIEWS #######################

def error_404(request):
    # merely forms
    return render(request, '404.html', {
    },
    )

def error_500(request):
    # merely forms
    return render(request, '500.html', {
    },
    )

# home page
# Maybe don't login_require this, and allow anonymous users to browse a
# list of currently posted books? idk.
@login_required
def index(request):

    # ability to create and display saved searches
    # pull all comments from listings user has posted on and their listings
    # make pagination work
    # NEED TO HAVE THE SEARCH WORK--- YAY HAYSTACK

    listings = []

    return render(request, 'index.html', {
        'listings' : listing,
    },
    )


# User's lookouts page.
@login_required
def lookouts(request, username):

    return render(request, 'lookouts.html', {

    },
    )

# User profile page
@login_required
def profile(request, username):

    # verify that the user exists
    seller = get_object_or_404(Seller, user__username=username)
    listings = Listing.objects.filter(seller__user__username=username)
    lookouts = Lookout.objects.filter(owner__user__username=username)
    FinalPrice_form = FinalPriceForm()

    return render(request, 'profile.html', {
        'seller' : seller,
        'listings': listings,
        'lookouts': lookouts,
        'total_sold' : totalSold( username ),
        'FinalPrice_form' : FinalPrice_form,
    },
    )

# Listing page
@login_required
def listing(request, username, book_id):

    seller = get_object_or_404(Seller,user__username=username)
    listing = get_object_or_404(Listing,pk=book_id)

    # if the listing is over a week old, it's old
    old_threshold = timezone.now() - timedelta(weeks=3)

    # get all bids associated with this listing
    bids = Bid.objects.filter( listing = listing )
    bid_count = len(bids)

    # make a thumbnail of the image
    # note: make sure to check if a thumbnail already exists tho!!
#    from PIL import Image
#    size = (100, 100)
#    image = Image.open( listing.photo )
#    image.thumbnail(size, Image.ANTIALIAS)
#    background = Image.new('RGBA', size, (255, 255, 255, 0))
#    background.paste( image,
#        ((size[0] - image.size[0]) / 2, (size[1] - image.size[1]) / 2))

    if listing.seller != seller:
        raise Http404("Seller does not match listing.")

    bid_form = BidForm()
    if request.method == 'POST':
        bid_form = BidForm( request.POST )
        if bid_form.is_valid():
            bid = bid_form.save(commit=False)
            bid.bidder = request.user.seller
            bid.listing = listing
            bid.save()
 
            return redirect( 'listing', listing.seller.user.username, listing.pk )

    return render(request, 'listing.html', {
        'listing' : listing,
        'media' : settings.MEDIA_URL,
        'old' : listing.date_created < old_threshold,
        'bid_count' : bid_count,
        'bids' : bids,
        'bid_form' : bid_form,
#        'thumbnail' : background,
    },
    )

@login_required
def create_listing(request):

    if request.method == 'POST':
        listing_form = ListingForm(request.POST, request.FILES, request=request)
        if listing_form.is_valid():
            listing = listing_form.save(commit=False)

            # Trim unnecessary whitespace chars from the sides.
            listing.title = listing.title.strip()
            listing.author = listing.author.strip()
            listing.edition = listing.edition.strip()

            # Trim the word "by" if it starts the author field.
            if len(listing.author) >= 2 and listing.author[:2].lower() == "by":
                listing.author = listing.author[2:]

            listing.seller = request.user.seller
            listing.save()

            return redirect( 'listing', listing.seller.user.username, listing.pk )
    else:
        listing_form = ListingForm(request=request)

    return render(request, 'create_listing.html', {
        'form' : listing_form,
    },
    )

@login_required
def close_listing(request, book_id):
    user = request.user
    listing = Listing.objects.get(pk=book_id)

    if listing.seller.user == user:
        listing.active = False
        listing.save()

    return redirect('profile', request.user.username)


@login_required
def sell_listing(request, book_id):
    user = request.user
    listing = Listing.objects.get(pk=book_id)

    if listing.seller.user == user:

        if request.method == 'POST':
            finalPrice_form = FinalPriceForm( request.POST )
            if finalPrice_form.is_valid():
                try:
                    listing.finalPrice = int(finalPrice_form.cleaned_data['final_price'])
                except ValueError, TypeError:
                    listing.finalPrice = listing.price

        listing.sold = True
        listing.active = False
        listing.save()

    return redirect('profile', request.user.username)


@login_required
def search(request):
    # merely forms
    return render(request, 'search.html', {
    
    },
    )

def about(request):
    # merely forms
    return render(request, 'about.html', {
    },
    )

def contact(request):
    # merely forms
    return render(request, 'contact.html', {
    },
    )

def privacy(request):
    # merely forms
    return render(request, 'privacy.html', {
    },
    )
