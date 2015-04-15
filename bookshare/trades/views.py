from trades.models import Listing, Bid, Flag
from trades.forms import ListingForm, BidForm, FlagForm, SellListingForm, UnSellListingForm, CancelListingForm, ReopenListingForm
from core.models import Student

from django.views.generic import View, DetailView, ListView, CreateView, UpdateView, DeleteView

from braces.views import LoginRequiredMixin

from django.contrib.auth.models import User
from django.http import Http404, HttpResponseForbidden
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
    paginate_by = 15
    queryset=Listing.objects.exclude(cancelled=True).order_by('-created')
    template_name = 'list_listings.html'
    login_url = '/'

class CreateListing(LoginRequiredMixin, CreateView):
    model = Listing
    fields = ['isbn', 'title', 'author', 'edition', 'year', 'condition',
        'access_code', 'price', 'photo', 'description']
    template_name = 'create_listing.html'
    context_object_name = 'listing'
    # ISBN query!
    login_url = '/'

    def form_valid(self, form):
        me = Student.objects.get(user=self.request.user)

        form.instance.seller = me
        return super(CreateListing, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateListing, self).get_context_data(**kwargs)

        form = ListingForm()
        context['my_form'] = form
        return context

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
        form = BidForm(initial={'listing': self.get_object()})
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
    fields = ['listing', 'price', 'text',]
    context_object_name = 'bid'
    template_name = 'detail_listing.html'
    login_url = '/'

    def form_valid(self, form):
        me = Student.objects.get(user=self.request.user)

        form.instance.bidder = me
        return super(CreateBid, self).form_valid(form)

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
    fields = ['reason',]
    template_name = 'create_flag.html'
    context_object_name = 'flag'

    login_url = '/'

    def form_valid(self, form):
        me = Student.objects.get(user=self.request.user)

        current_url = self.request.get_full_path()
        listing_slug = current_url.split('/')[3]
        # [u'', u'share', u'listing', u'C1s3oD', u'flag']
        selected_listing = Listing.objects.get(slug=listing_slug)

        form.instance.flagger = me
        form.instance.listing = selected_listing
        return super(CreateFlag, self).form_valid(form)

    def get_success_url(self):
        return reverse('detail_listing', kwargs={'slug':self.object.listing.slug})

    def get_context_data(self, **kwargs):
        context = super(CreateFlag, self).get_context_data(**kwargs)
        me = Student.objects.get(user=self.request.user)

        # duplicated code!!!
        current_url = self.request.get_full_path()
        listing_slug = current_url.split('/')[3]
        # [u'', u'share', u'listing', u'C1s3oD', u'flag']
        selected_listing = Listing.objects.get(slug=listing_slug)

        selling_student = selected_listing.seller

        # you can't flag your own listing
        if (selling_student == me):
            return HttpResponseForbidden()

        # can only create a flag if you haven't previously created one
        if not can_flag(me, selected_listing):
            # because the page shouldn't exist in this scenario
            raise Http404

        context['listing'] = selected_listing

        form = FlagForm()
        context['my_form'] = form
        return context

class DeleteFlag(LoginRequiredMixin, DeleteView):
    model = Flag
    context_object_name = 'flag'
    template_name = 'delete_flag.html'

    def get_success_url(self):
        return reverse('detail_listing', kwargs={'slug':self.object.listing.slug})

    def get_context_data(self, **kwargs):
        context = super(DeleteFlag, self).get_context_data(**kwargs)
        me = Student.objects.get(user=self.request.user)

        flag_student = self.get_object().flagger

        # if you didn't create the flag, you can't delete the flag
        if not(me == flag_student):
            return HttpResponseForbidden()

        return context

class DeleteBid(LoginRequiredMixin, DeleteView):
    model = Bid
    success_url = '/'

    # can be deleted by either creator or person for lister

class EditBid(LoginRequiredMixin, UpdateView):
    model = Bid
    success_url = '/'

    # can only be edited by the bidder

class EditListing(LoginRequiredMixin, UpdateView):
    model = Listing
    template_name = 'listing_edit.html'
    context_object_name = 'listing'
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
            return HttpResponseForbidden()

        return context 

class SellListing(LoginRequiredMixin, UpdateView):
    model = Listing
    fields = ['email_message', 'winning_bid',]
    template_suffix_name = '_sell'
    context_object_name = 'listing'
    template_name = 'listing_sell.html'

    login_url = '/'

    def form_valid(self, form):
        today = date.today()

        form.instance.sold = True
        form.instance.date_closed = today
        return super(SellListing, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SellListing, self).get_context_data(**kwargs)

        me = Student.objects.get(user=self.request.user)
        selling_student = self.get_object().seller

        if not(selling_student == me):
            return HttpResponseForbidden()

        bid_count = Bid.objects.filter(listing=self.get_object).count()
        if bid_count < 1:
            # because the page shouldn't exist in this scenario
            raise Http404

        form = SellListingForm()
        form.fields['winning_bid'].queryset = Bid.objects.filter(listing=self.get_object())

        context['my_form'] = form

        return context 

class UnSellListing(LoginRequiredMixin, UpdateView):
    model = Listing
    fields = []
    template_suffix_name = '_unsell'
    context_object_name = 'listing'
    template_name = 'listing_unsell.html'

    login_url = '/'

    def form_valid(self, form):
        form.instance.sold = False
        form.instance.date_closed = None
        form.instance.winning_bid = None
        return super(UnSellListing, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UnSellListing, self).get_context_data(**kwargs)

        me = Student.objects.get(user=self.request.user)
        selling_student = self.get_object().seller

        if not(selling_student == me):
            return HttpResponseForbidden()

        form = UnSellListingForm()
        context['my_form'] = form

        return context 

class CancelListing(LoginRequiredMixin, UpdateView):
    model = Listing
    fields = []
    template_suffix_name = '_cancel'
    context_object_name = 'listing'
    template_name = 'listing_cancel.html'

    login_url = '/'

    def form_valid(self, form):
        today = date.today()

        form.instance.cancelled = True
        form.instance.date_closed = today
        return super(CancelListing, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CancelListing, self).get_context_data(**kwargs)

        me = Student.objects.get(user=self.request.user)
        selling_student = self.get_object().seller

        if not(selling_student == me):
            return HttpResponseForbidden()

        today = date.today()

        form = CancelListingForm()
        context['my_form'] = form

        return context 

class ReopenListing(LoginRequiredMixin, UpdateView):
    model = Listing
    fields = []
    template_suffix_name = '_reopen'
    context_object_name = 'listing'
    template_name = 'listing_reopen.html'

    login_url = '/'

    def form_valid(self, form):
        form.instance.cancelled = False
        form.instance.date_closed = None
        return super(ReopenListing, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ReopenListing, self).get_context_data(**kwargs)

        me = Student.objects.get(user=self.request.user)
        selling_student = self.get_object().seller

        if not(selling_student == me):
            return HttpResponseForbidden()

        form = ReopenListingForm()
        context['my_form'] = form

        return context 
