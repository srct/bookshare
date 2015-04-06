from trades.models import Listing, Bid, Flag
from trades.forms import ListingForm, BidForm, FlagForm, SellListingForm, UnSellListingForm, CancelListingForm, ReopenListingForm
from core.models import Student

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

# flagging
# you can only flag a listing once...
def can_flag(flagger, listing):
    user_flag_num = Flag.objects.filter(flagger=flagger, listing=listing).count()
    # we're assuming that this isn't going to go over 1
    if user_flag_num:
        return False
    else:
        return True

# get the listing's slug to pass to the create flag page
def flag_slug(flagger, listing):
    if not can_flag(flagger, listing):
        return Flag.objects.get(flagger=flagger, listing=listing).slug
    else:
        return None

# validation of new listing forms
    # <3 test cases

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
        me = Student.objects.get(user=self.request.user)

        # make the form available to the template on get
        # set the bidder and the listing
        form = BidForm(initial={'bidder' : me, 'listing' : self.get_object()})
        #form.fields['bidder'].widget = HiddenInput()
        form.fields['listing'].widget = HiddenInput()

        context['my_form'] = form

        # bids, filter by listing name of the current listing, order by date created
        context['bids'] = Bid.objects.filter(listing=self.get_object()).order_by('-price')
        context['bid_count'] = Bid.objects.filter(listing=self.get_object).count()
        # flags
        context['flags'] = Flag.objects.filter(listing=self.get_object()).order_by('-created')
        context['flag_count'] = Flag.objects.filter(listing=self.get_object()).count()
        context['can_flag'] = can_flag(me, self.get_object())
        context['flag_slug'] = flag_slug(me, self.get_object())
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

class CreateFlag(LoginRequiredMixin, CreateView):
    model = Flag
    template_name = 'create_flag.html'

    login_url = '/'

    def get_success_url(self):
        return reverse('detail_listing', kwargs={'slug':self.object.listing.slug})

    def get_context_data(self, **kwargs):
        context = super(CreateFlag, self).get_context_data(**kwargs)
        me = Student.objects.get(user=self.request.user)

        current_url = self.request.get_full_path()
        listing_slug = current_url.split('/')[3]
        # [u'', u'share', u'listing', u'C1s3oD', u'flag']
        selected_listing = Listing.objects.get(slug=listing_slug)

        form = FlagForm(initial={'flagger' : me, 'listing' : selected_listing})

        context['my_form'] = form

        selling_student = selected_listing.seller

        # you can't flag your own listing
        if (selling_student == me):
            raise Http404

        # can only create a flag if you haven't previously created one
        if not can_flag(me, selected_listing):
           raise Http404

        context['listing'] = selected_listing
        return context

class DeleteFlag(LoginRequiredMixin, DeleteView):
    model = Flag
    template_name = 'delete_flag.html'

    def get_success_url(self):
        return reverse('detail_listing', kwargs={'slug':self.object.listing.slug})

    def get_context_data(self, **kwargs):
        context = super(DeleteFlag, self).get_context_data(**kwargs)
        me = Student.objects.get(user=self.request.user)

        flag_student = self.get_object().flagger.user

#if not(requesting_student == flag_student):
#            raise Http404

        return context

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

        me = Student.objects.get(user=self.request.user)

        form = ListingForm(initial={'seller' : me})
        #form.fields['seller'].widget = HiddenInput()

        context['my_form'] = form

        return context

class EditListing(LoginRequiredMixin, UpdateView):
    model = Listing
    #form_class = EditListingForm

    fields = ['title', 'author', 'isbn', 'year', 'edition', 'condition', 'access_code',
        'description', 'price', 'photo',]
    template_suffix_name = '_edit'

    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(EditListing, self).get_context_data(**kwargs)

        me = Student.objects.get(user=self.request.user)
        selling_student = self.get_object().seller

        if not(selling_student == me):
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

        me = Student.objects.get(user=self.request.user)
        selling_student = self.get_object().seller

        if not(selling_student == me):
            raise Http404

        today = date.today()

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

        me = Student.objects.get(user=self.request.user)
        selling_student = self.get_object().seller

        if not(selling_student == me):
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

        me = Student.objects.get(user=self.request.user)
        selling_student = self.get_object().seller

        if not(selling_student == me):
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

        me = Student.objects.get(user=self.request.user)
        selling_student = self.get_object().seller

        if not(selling_student == me):
            raise Http404

        form = ReopenListingForm(initial={'cancelled' : False})
        form.fields['cancelled'].widget = HiddenInput()

        context['my_form'] = form

        return context 
