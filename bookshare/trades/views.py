from trades.models import Listing, Bid
from trades.forms import ListingForm, FinalPriceForm, CloseForm, BidForm

from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from braces.views import LoginRequiredMixin

from django.contrib.auth.models import User
from django.http import Http404

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
    login_url = '/'

class DetailListing(LoginRequiredMixin, DetailView):
    model = Listing
    context_object_name = 'listing'

    # see this for the bidding form
    # https://docs.djangoproject.com/en/1.7/topics/class-based-views/mixins/#an-alternative-better-solution

    # further need to incorporate much of the logic below somewhere
    # - bid count
    # - bid's age, then if 'old'
    # - whether it's the person who posted the bid or someone else

    def get_context_data(self, **kwargs):
        context = super(DetailListing, self).get_context_data(**kwargs)
        # bids, filter by listing name of the current listing, order by date created
        context['bids'] = Bid.objects.filter(listing=self.get_object()).order_by('-created')
        return context 

    login_url = '/'

class CreateListing(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm
    # ISBN query!
    #success_url = '/'
    login_url = '/'

"""
    # if the listing is over a week old, it's old
    old_threshold = timezone.now() - timedelta(weeks=3)

    # get all trades associated with this listing
    bids = Bid.objects.filter( listing = listing )
    bid_count = len(bids)


    return render(request, 'listing.html', {
        'listing' : listing,
        'media' : settings.MEDIA_URL,
        'old' : listing.date_created < old_threshold,
        'bid_count' : bid_count,
        'trades' : bids,
        'bid_form' : bid_form,
    },
    )
"""

class UpdateListing(LoginRequiredMixin, UpdateView):
    model = Listing
    #form_class = UpdateListingForm

    fields = ['active', 'title', 'author', 'isbn', 'year', 'edition', 'condition',
        'description', 'price', 'photo',]
    template_suffix_name = '_update'

    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(UpdateListing, self).get_context_data(**kwargs)

        requesting_student = User.objects.get(username=self.request.user.username)
        selling_student = self.get_object().seller.user

        print requesting_student
        print selling_student

#        if selling_student is not requesting_student:
#            raise Http404

        return context 

class CloseListing(LoginRequiredMixin, UpdateView):
    model = Listing
    fields = ['sold', 'date_sold', 'finalPrice',]
    template_suffix_name = '_close'

    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(CloseListing, self).get_context_data(**kwargs)

        requesting_student = User.objects.get(username=self.request.user.username)
        selling_student = self.get_object().seller.user

        print requesting_student
        print selling_student

#        if selling_student is not requesting_student:
#            raise Http404

        return context 

