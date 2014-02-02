from website.models import Listing,Seller
from website.forms import ListingForm, FinalPriceForm, CloseForm
from bids.models import Bid
from bids.forms import BidForm
from lookouts.models import Lookout
from lookouts.forms import LookoutForm, DeleteLookoutForm

from django.http import Http404
from django.conf import settings
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from datetime import datetime,timedelta
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory

import math
import pyisbn
import requests

# pulls worldcat metadata from ISBNs
def ISBNMetadata(standardISBN):
    url = "http://xisbn.worldcat.org/webservices/xid/isbn/" + str(standardISBN) + "?method=getMetadata&format=json&fl=title,year,author,ed"
    metadata = requests.get(url)
    # format into a dictionary
    dejson = metadata.json()
    try:
        metadataDict = dejson.get('list')
        return metadataDict[0]
    except:
        return None

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
@login_required
def index(request):

    lookouts = Lookout.objects.filter(
        owner__user__username = request.user.username )

    # This unwieldy double forloop grabs the pk of each listing that shows
    # up for your lookout, and adds it to a list.
    listing_pks = []
    for lookout in lookouts:
        lookout_listings = lookout.get_listings()
        for lookout_listing in lookout_listings:
            listing_pks.append( lookout_listing.pk )

    # The list of pks is then used to create a queryset, ordered by newest
    # listing first.
    listings = Listing.objects.filter(pk__in=listing_pks).order_by('-date_created')

    # Listings will be shown in 3 columns and 2 rows, for a total of 6
    # entries per page.
    paginator = Paginator(listings, 6) # Show 6 listings per page

    page = request.GET.get('page')
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        # if page is NaN, deliver the first page
        listings = paginator.page(1)
    except EmptyPage:
        # if the page is empty, deliver the last page
        listings = paginator.page(paginator.num_pages)

    # the rows variable is >= 1, and is determined by the number of
    # entries on this page. this is intended to cause the listing
    # previews to fill in rows first, rather than columns.
    rows = int(math.ceil( len(listings) / 3.0 )) or 1

    return render(request, 'index.html', {
        'listings' : listings,
        'rows' : rows,
    },
    )

# User profile page
@login_required
def profile(request, username):

    # verify that the user exists
    seller = get_object_or_404(Seller, user__username=username)
    listings = Listing.objects.filter(seller__user__username=username)
    lookouts = Lookout.objects.filter(owner__user__username=username)
    FinalPrice_form = FinalPriceForm(prefix="finalPrice")
    close_form = CloseForm(prefix="close")
    DeleteLookout_form = DeleteLookoutForm()
    lookout_form = LookoutForm()

    if request.method == 'POST':
        # Parse the ClosedForm input fields
        if 'closed' in request.POST:
            close_form = CloseForm( request.POST, prefix="close" )
            if close_form.is_valid():
                book_id = close_form.cleaned_data.get('book_id')
                listing = Listing.objects.get(pk=book_id)
                if listing.seller == request.user.seller:
                    listing.active = False
                    listing.save()
                    return redirect('profile', username)
                else:
                    raise PermissionDenied("You do not own this listing.")
        # Parse the FinalPriceForm input fields
        elif 'sold' in request.POST:
            FinalPrice_form = FinalPriceForm( request.POST, prefix="finalPrice" )
            if FinalPrice_form.is_valid():
                book_id = FinalPrice_form.cleaned_data.get('book_id')
                listing = Listing.objects.get(pk=book_id)
                try:
                    final_price = int(FinalPrice_form.cleaned_data.get('final_price'))
                except ValueError, TypeError:
                    final_price = 0
                if listing.seller == request.user.seller:
                    listing.finalPrice = final_price
                    listing.sold = True
                    listing.active = False
                    listing.save()
                    return redirect('profile', username)
                else:
                    raise PermissionDenied("You do not own this listing.")
        # Parse the DeleteLookoutForm input fields
        elif 'lookout' in request.POST:
            DeleteLookout_form = DeleteLookoutForm( request.POST )
            if DeleteLookout_form.is_valid():
                lookout_id = DeleteLookout_form.cleaned_data.get('lookout_id')
                lookout = Lookout.objects.get(pk=lookout_id)
                if lookout.owner == request.user.seller:
                    lookout.delete()
                    return redirect('profile', username)
                else:
                    raise PermissionDenied("You do not own this lookout.")
        elif 'lookout-create' in request.POST:
            lookout_form = LookoutForm( request.POST )
            if lookout_form.is_valid():
                lookout = lookout_form.save(commit=False)
                lookout.ISBN = lookout.ISBN.strip()
                lookout.owner = request.user.seller
                lookout.save()
                return redirect( 'profile', username )

    return render(request, 'profile.html', {
        'seller' : seller,
        'listings': listings,
        'lookouts': lookouts,
        'total_sold' : totalSold( username ),
        'FinalPrice_form' : FinalPrice_form,
        'close_form' : close_form,
        'DeleteLookout_form' : DeleteLookout_form,
        'CreateLookout_form': lookout_form,
    },
    )


@login_required
def create_lookout(request, username):

    lookout_form = LookoutForm()

    if request.method == 'POST':
        lookout_form = LookoutForm( request.POST )
        if lookout_form.is_valid():
            lookout = lookout_form.save(commit=False)
            lookout.ISBN = lookout.ISBN.strip()
            lookout.owner = request.user.seller
            lookout.save()
            return redirect( 'profile', username )

    return render(request, 'create_lookout.html', {
        'lookout_form': lookout_form,
    },
    )


@login_required
def all_listings(request):
    # The list of pks is then used to create a queryset, ordered by newest
    # listing first.
    listings = Listing.objects.all().order_by('-date_created')

    # Listings will be shown in 3 columns and 2 rows, for a total of 6
    # entries per page.
    paginator = Paginator(listings, 6) # Show 6 listings per page

    page = request.GET.get('page')
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        # if page is NaN, deliver the first page
        listings = paginator.page(1)
    except EmptyPage:
        # if the page is empty, deliver the last page
        listings = paginator.page(paginator.num_pages)

    # the rows variable is >= 1, and is determined by the number of
    # entries on this page. this is intended to cause the listing
    # previews to fill in rows first, rather than columns.
    rows = int(math.ceil( len(listings) / 3.0 )) or 1

    return render(request, 'all_listings.html', {
        'listings' : listings,
        'rows' : rows,
    },
    )


# Listing page
@login_required
def view_listing(request, book_id):

    # Grab the listing itself
    listing = get_object_or_404(Listing,pk=book_id)

    # grab the bidder
    bidder = request.user.seller

    # if the listing is over a week old, it's old
    old_threshold = timezone.now() - timedelta(weeks=3)

    # get all bids associated with this listing
    bids = Bid.objects.filter( listing = listing )
    bid_count = len(bids)

    bid_form = BidForm()
    if request.method == 'POST' and listing.active and not listing.sold:
        if listing.active and not listing.sold:
            bid_form = BidForm( request.POST.copy() )

            # Override whatever the user may have input into the bidder and
            # listing fields (hopefully they will not have set these values
            # anyway).
            bid_form.data['bidder'] = bidder.pk
            bid_form.data['listing'] = listing.pk

            if bid_form.is_valid():
                bid = bid_form.save(commit=False)
                bid.bidder = bidder
                bid.listing = listing
                bid.full_clean()
                bid.save()
                return redirect( 'view_listing', listing.pk )

    return render(request, 'listing.html', {
        'listing' : listing,
        'media' : settings.MEDIA_URL,
        'old' : listing.date_created < old_threshold,
        'bid_count' : bid_count,
        'bids' : bids,
        'bid_form' : bid_form,
    },
    )

# Allow user to create a listing
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

            return redirect( 'view_listing', listing.pk )
    else:
        listing_form = ListingForm(request=request)

    return render(request, 'create_listing.html', {
        'form' : listing_form,
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

def privacy_opt_out(request):
    # merely forms
    return render(request, 'privacy_opt_out.html', {
    },
    )

@login_required
def search(request):
    # merely forms
    return render(request, 'search.html', {
    },
    )

