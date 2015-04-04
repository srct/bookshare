from trades.models import Listing, Bid
from trades.forms import ListingForm, BidForm, SellListingForm, UnSellListingForm, CancelListingForm, ReopenListingForm

from django.views.generic import View, DetailView, ListView, CreateView, UpdateView, DeleteView

from braces.views import LoginRequiredMixin

from django.contrib.auth.models import User
from django.http import Http404
from django.forms.widgets import HiddenInput
from django.core.urlresolvers import reverse

import math
import pyisbn
import requests
from datetime import date

# pulls worldcat metadata from ISBNs
def ISBNMetadata(standardISBN):
    # passing in numbers starting with 0 throws "SyntaxError: invalid token"
    url = "http://xisbn.worldcat.org/webservices/xid/isbn/" + str(standardISBN) + "?method=getMetadata&format=json&fl=title,year,author,ed"
    metadata = requests.get(url)
    # format into a dictionary
    dejson = metadata.json()
    try:
        metadataDict = dejson.get('list')
        return metadataDict[0]
    except:
        return None

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

# These next two views are tied together...
class DetailListing(DetailView):
    model = Listing
    context_object_name = 'listing'
    template_name = 'detail_listing.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(DetailListing, self).get_context_data(**kwargs)
        me = User.objects.get(username=self.request.user.username)

        # make the form available to the template on get
        # set the bidder and the listing
        form = BidForm(initial={'bidder' : me, 'listing' : self.get_object()})
        #form.fields['bidder'].widget = HiddenInput()
        form.fields['listing'].widget = HiddenInput()

        context['my_form'] = form

        # bids, filter by listing name of the current listing, order by date created
        context['bids'] = Bid.objects.filter(listing=self.get_object()).order_by('-price')
        context['bid_count'] = len(Bid.objects.filter(listing=self.get_object))
        return context 

class CreateBid(CreateView):
    model = Bid
    form_class = BidForm
    template_name = 'detail_listing.html'
    login_url = '/'

    def get_success_url(self):
        return reverse('detail_listing', kwargs={'slug':self.object.listing.slug})

# ...to make this single view
class ListingPage(LoginRequiredMixin, View):

    # see this page for an explanation
    # https://docs.djangoproject.com/en/1.7/topics/class-based-views/mixins/#an-alternative-better-solution

    def get(self, request, *args, **kwargs):
        view = DetailListing.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CreateBid.as_view()
        return view(request, *args, **kwargs)

# and we return to our regularly schedule programming
class DeleteBid(LoginRequiredMixin, DeleteView):
    model = Bid
    success_url = '/'

    # can be deleted by either creator or person for lister

class EditBid(LoginRequiredMixin, UpdateView):
    model = Bid
    success_url = '/'

    # can only be edited by the bidder

class CreateListing(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm
    # ISBN query!
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(CreateListing, self).get_context_data(**kwargs)

        me = Student.objects.get(username=self.request.user.username)

        form = ListingForm(initial={'seller' : me})
        #form.fields['seller'].widget = HiddenInput()

        context['my_form'] = form

        return context

class EditListing(LoginRequiredMixin, UpdateView):
    model = Listing
    #form_class = EditListingForm

    fields = ['title', 'author', 'isbn', 'year', 'edition', 'condition',
        'description', 'price', 'photo',]
    template_suffix_name = '_edit'

    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(EditListing, self).get_context_data(**kwargs)

        requesting_student = User.objects.get(username=self.request.user.username)
        selling_student = self.get_object().seller.user

        if not(selling_student == requesting_student):
            raise Http404

        return context 

class SellListing(LoginRequiredMixin, UpdateView):
    model = Listing
    fields = ['sold', 'email_message', 'winning_bid', 'date_closed']
    template_suffix_name = '_sell'
    form_class = SellListingForm

    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(SellListing, self).get_context_data(**kwargs)

        requesting_student = User.objects.get(username=self.request.user.username)
        selling_student = self.get_object().seller.user

        if not(selling_student == requesting_student):
            raise Http404

        today = date.today()
        # set default to highest price

        form = SellListingForm(initial={'sold' : True, 'date_closed' : today})
        form.fields['winning_bid'].queryset = Bid.objects.filter(listing=self.get_object())
        form.fields['winning_bid'].required = True
        form.fields['sold'].widget = HiddenInput()
        form.fields['date_closed'].widget = HiddenInput()

        context['my_form'] = form

        return context 

class UnSellListing(LoginRequiredMixin, UpdateView):
    model = Listing
    fields = ['sold', 'winning_bid', 'date_closed']
    template_suffix_name = '_unsell'
    form_class = UnSellListingForm

    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(UnSellListing, self).get_context_data(**kwargs)

        requesting_student = User.objects.get(username=self.request.user.username)
        selling_student = self.get_object().seller.user

        if not(selling_student == requesting_student):
            raise Http404

        today = date.today()

        form = UnSellListingForm(initial={'sold' : False, 'date_closed' : '', 'winning_bid' : ''})
        form.fields['sold'].widget = HiddenInput()
        form.fields['date_closed'].widget = HiddenInput()
        form.fields['winning_bid'].widget = HiddenInput()

        context['my_form'] = form

        return context 

class CancelListing(LoginRequiredMixin, UpdateView):
    model = Listing
    fields = ['cancelled', 'date_closed',]
    template_suffix_name = '_cancel'
    form_class = CancelListingForm

    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(CancelListing, self).get_context_data(**kwargs)

        requesting_student = User.objects.get(username=self.request.user.username)
        selling_student = self.get_object().seller.user

        if not(selling_student == requesting_student):
            raise Http404

        today = date.today()

        form = CancelListingForm(initial={'cancelled' : True, 'date_closed' : ''})
        form.fields['cancelled'].widget = HiddenInput()
        form.fields['date_closed'].widget = HiddenInput()

        context['my_form'] = form

        return context 

class ReopenListing(LoginRequiredMixin, UpdateView):
    model = Listing
    fields = ['cancelled']
    template_suffix_name = '_reopen'
    form_class = ReopenListingForm

    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(ReopenListing, self).get_context_data(**kwargs)

        requesting_student = User.objects.get(username=self.request.user.username)
        selling_student = self.get_object().seller.user

        if not(selling_student == requesting_student):
            raise Http404

        form = ReopenListingForm(initial={'cancelled' : False})
        form.fields['cancelled'].widget = HiddenInput()

        context['my_form'] = form

        return context 
