from trades.models import Listing, Bid
from trades.forms import ListingForm, FinalPriceForm, CloseForm, BidForm

from lookouts.models import Lookout
from lookouts.forms import LookoutForm, DeleteLookoutForm

# where is seller???

from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from braces.views import LoginRequiredMixin

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
    sellerListings = Listing.objects.filter(seller__user__username=seller).order_by("-created")
    # all listings that seller has commented on (preferably ordered in reverse)
    # put those lists together
    # return that list
    return False

### VIEWS ###

class ListListings(LoginRequiredMixin, ListView):
    model = Listing
    context_object_name = 'listings'
    queryset = Listing.objects.all().order_by('-created')
    paginate_by = 25
    login_url = '/'

# Listing page
def view_listing(request, book_id):

    # Grab the listing itself
    listing = get_object_or_404(Listing,pk=book_id)

    # grab the bidder
    bidder = request.user.seller

    # if the listing is over a week old, it's old
    old_threshold = timezone.now() - timedelta(weeks=3)

    # get all trades associated with this listing
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
        'trades' : bids,
        'bid_form' : bid_form,
    },
    )

class CreateListing(LoginRequiredMixin, CreateView):
    model = Listing,
    # actually create said form
#    form_class = CreateListingForm
    form_class = ListingForm
    success_url = '/'
    login_url = '/'
