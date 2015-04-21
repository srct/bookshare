# standard library imports
from datetime import date
from cStringIO import StringIO
# core django imports
from django.views.generic import View, DetailView, ListView, CreateView,\
    UpdateView, DeleteView
from django.http import Http404, HttpResponseForbidden
from django.forms.widgets import HiddenInput
from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib import messages
from django.utils.safestring import mark_safe
# third party imports
import requests
from PIL import Image
from braces.views import LoginRequiredMixin
from braces.views import FormValidMessageMixin
from ratelimit.decorators import ratelimit
# imports from your apps
from .models import Listing, Bid, Flag, Rating
from .forms import ListingForm, BidForm, FlagForm, SellListingForm,\
    UnSellListingForm, RatingForm
from core.models import Student


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
    user_flag_num = Flag.objects.filter(flagger=flagger,
                                        listing=listing).count()
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


# rating
# (basically) duplicated code!!!
def can_rate(rater, listing):
    user_rate_num = Rating.objects.filter(rater=rater,
                                           listing=listing).count()
    # we're assuming that this isn't going to go over 1
    if user_rate_num:
        return False
    else:
        return True


class ListListings(LoginRequiredMixin, ListView):
    model = Listing
    context_object_name = 'listings'
    paginate_by = 15
    queryset = Listing.objects.exclude(cancelled=True).order_by('-created')
    template_name = 'list_listings.html'
    login_url = 'login'


class CreateListing(LoginRequiredMixin, FormValidMessageMixin, CreateView):
    model = Listing
    fields = ['isbn', 'title', 'author', 'edition', 'year', 'course_abbr',
              'condition', 'access_code', 'price', 'photo', 'description']
    template_name = 'create_listing.html'
    context_object_name = 'listing'
    # ISBN query!
    login_url = 'login'

    # eventually figure out how to use {% url 'create_listing' %}
    form_valid_message = mark_safe("""Your listing was successfully created!
                         <a href="/share/new/">Create another here!</a>""")

    def form_valid(self, form):
        me = Student.objects.get(user=self.request.user)

        form.instance.seller = me

        image_name = form.instance.photo.name
        user_image = Image.open(form.instance.photo)
        image_format = user_image.format

        print user_image
        width, height = user_image.size
        print user_image.size
        print width, "width"
        print height, "height"
        maxsize = (2560, 1920)
        # five megapixels is 2560x1920
        if (width > 2560) or (height > 1920):
            user_image.thumbnail(maxsize)

            temp_image = StringIO()
            user_image.save(temp_image, image_format)
            temp_image.seek(0)

            new_uploaded_file = SimpleUploadedFile(image_name,
                            temp_image.read(), content_type=image_format)

            form.instance.photo = new_uploaded_file

        return super(CreateListing, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateListing, self).get_context_data(**kwargs)

        form = ListingForm()
        context['my_form'] = form
        return context

    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    @ratelimit(key='user', rate='100/day', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(CreateListing, self).post(request, *args, **kwargs)


# These next two views are tied together...
class DetailListing(DetailView):
    model = Listing
    context_object_name = 'listing'
    template_name = 'detail_listing.html'

    def get_context_data(self, **kwargs):
        context = super(DetailListing, self).get_context_data(**kwargs)
        me = Student.objects.get(user=self.request.user)

        # make the form available to the template on get
        # set the bidder and the listing
        form = BidForm(initial={'listing': self.get_object()})
        form.fields['listing'].widget = HiddenInput()
        context['my_form'] = form

        try:
            context['rating'] = Rating.objects.get(listing=self.get_object())
        except:
            context['rating'] = False

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
    fields = ['listing', 'price', 'text', ]
    context_object_name = 'bid'
    template_name = 'detail_listing.html'

    def form_valid(self, form):
        me = Student.objects.get(user=self.request.user)

        form.instance.bidder = me
        return super(CreateBid, self).form_valid(form)

    def get_success_url(self):
        return reverse('detail_listing',
                       kwargs={'slug': self.object.listing.slug})


# ...to make this single view
class ListingPage(LoginRequiredMixin, View):
    login_url = 'login'

    # see this page for an explanation
    # https://docs.djangoproject.com/en/1.7/topics/class-based-views/mixins/#an-alternative-better-solution

    def get(self, request, *args, **kwargs):
        view = DetailListing.as_view()
        return view(request, *args, **kwargs)

    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    # rate limit is higher for bids
    @ratelimit(key='user', rate='200/d', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        view = CreateBid.as_view()
        return view(request, *args, **kwargs)


# and we return to our regularly schedule programming
class CreateFlag(LoginRequiredMixin, CreateView):
    model = Flag
    fields = ['reason', ]
    template_name = 'create_flag.html'
    context_object_name = 'flag'
    login_url = 'login'

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
        return reverse('detail_listing',
                       kwargs={'slug': self.object.listing.slug})

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

    # no daily limit because we want people to flag everything they need to
    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(CreateFlag, self).post(request, *args, **kwargs)


class DeleteFlag(LoginRequiredMixin, DeleteView):
    model = Flag
    context_object_name = 'flag'
    template_name = 'delete_flag.html'
    login_url = 'login'

    def get_success_url(self):
        return reverse('detail_listing',
                       kwargs={'slug': self.object.listing.slug})

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


class EditListing(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    model = Listing
    template_name = 'listing_edit.html'
    context_object_name = 'listing'
    #form_class = EditListingForm
    login_url = 'login'

    form_valid_message = "Your listing was successfully updated!"

    fields = ['title', 'author', 'isbn', 'year', 'edition', 'condition',
              'access_code', 'description', 'price', 'photo', ]
    template_suffix_name = '_edit'

    def get_context_data(self, **kwargs):
        context = super(EditListing, self).get_context_data(**kwargs)

        me = Student.objects.get(user=self.request.user)
        selling_student = self.get_object().seller

        if not(selling_student == me):
            return HttpResponseForbidden()

        return context


class SellListing(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    model = Listing
    fields = ['email_message', 'winning_bid', ]
    template_suffix_name = '_sell'
    context_object_name = 'listing'
    template_name = 'listing_sell.html'
    login_url = 'login'

    form_valid_message = "Your email was successfully sent!"

    def form_valid(self, form):
        # filling out fields
        today = date.today()
        self.obj = self.get_object()

        form.instance.sold = True
        form.instance.date_closed = today

        # sending email
        # I'm still second guessing as to whether this should be in this method
        text_email = get_template('email/sold.txt')
        html_email = get_template('email/sold.html')

        email_context = Context({
            'bidder_first_name': form.instance.winning_bid.bidder.user.first_name,
            'seller_name': self.obj.seller.user.get_full_name(),
            'bid_num': form.instance.winning_bid.price,
            'listing_title': self.obj.title,
            'seller_email': self.obj.seller.user.email,
            'email_message': form.instance.email_message, })

        subject, from_email, to, cc = ('Your bid has been selected on Bookshare!',
                                       'no-reply@bookshare.srct.io',
                                       #form.instance.winning_bid.bidder.user.email,
                                       #self.obj.seller.user.email)
                                       'success@simulator.amazonses.com',
                                       'success@simulator.amazonses.com')
        text_content = text_email.render(email_context)
        html_content = html_email.render(email_context)
        msg = EmailMultiAlternatives(subject, text_content,
                                     from_email, [to], [cc])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

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

    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    @ratelimit(key='user', rate='100/d', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(SellListing, self).post(request, *args, **kwargs)


class UnSellListing(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    model = Listing
    fields = ['email_message', ]
    template_suffix_name = '_unsell'
    context_object_name = 'listing'
    template_name = 'listing_unsell.html'
    login_url = 'login'

    form_valid_message = """Your sale has been successfully cancelled,
                     and your email successfully sent!"""

    def form_valid(self, form):
        self.obj = self.get_object()
        text_email = get_template('email/unsold.txt')
        html_email = get_template('email/unsold.html')

        email_context = Context({
            'bidder_first_name': self.obj.winning_bid.bidder.user.first_name,
            'seller_name': self.obj.seller.user.get_full_name(),
            'bid_num': self.obj.winning_bid.price,
            'listing_title': self.obj.title,
            'seller_email': self.obj.seller.user.email,
            'seller_email': form.instance.email_message, })

        subject, from_email, to, cc = ('Your transaction has been cancelled on Bookshare',
                                       'no-reply@bookshare.srct.io',
                                       #self.obj.winning_bid.bidder.user.email,
                                       #self.obj.seller.user.email)
                                       'success@simulator.amazonses.com',
                                       'success@simulator.amazonses.com')
        text_content = text_email.render(email_context)
        html_content = html_email.render(email_context)
        msg = EmailMultiAlternatives(subject, text_content,
                                     from_email, [to], [cc])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # this has to come after the email has been sent, otherwise these are
        # cleaned out 
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
 
    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    @ratelimit(key='user', rate='100/d', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(UnSellListing, self).post(request, *args, **kwargs)


class CancelListing(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    model = Listing
    fields = []
    template_suffix_name = '_cancel'
    context_object_name = 'listing'
    template_name = 'listing_cancel.html'
    login_url = 'login'

    form_valid_message = "Your listing was successfully cancelled!"

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

        return context


class ReopenListing(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    model = Listing
    fields = []
    template_suffix_name = '_reopen'
    context_object_name = 'listing'
    template_name = 'listing_reopen.html'
    login_url = 'login'

    form_valid_message = "Your listing was successfully reopened!"

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

        return context


class CreateRating(LoginRequiredMixin, CreateView):
    model = Rating
    fields = ['stars', 'review', ]
    template_name = 'create_rating.html'
    context_object_name = 'rating'
    login_url = 'login'

    def form_valid(self, form):
        me = Student.objects.get(user=self.request.user)

        current_url = self.request.get_full_path()
        listing_slug = current_url.split('/')[3]
        # [u'', u'share', u'listing', u'C1s3oD', u'flag']
        selected_listing = Listing.objects.get(slug=listing_slug)

        form.instance.rater = me
        form.instance.listing = selected_listing
        return super(CreateRating, self).form_valid(form)

    def get_success_url(self):
        return reverse('ratings',
                       kwargs={'slug': self.object.listing.seller.slug})

    def get_context_data(self, **kwargs):
        context = super(CreateRating, self).get_context_data(**kwargs)
        me = Student.objects.get(user=self.request.user)

        # duplicated code!!!
        current_url = self.request.get_full_path()
        listing_slug = current_url.split('/')[3]
        # [u'', u'share', u'listing', u'C1s3oD', u'flag']
        selected_listing = Listing.objects.get(slug=listing_slug)

        winning_student = selected_listing.winning_bid.bidder

        # you can only rate a listing that you won
        if not (winning_student == me):
            return HttpResponseForbidden()

        # can only create a rating if you haven't previously created one
        if not can_rate(me, selected_listing):
            # because the page shouldn't exist in this scenario
            raise Http404

        context['listing'] = selected_listing

        form = RatingForm()
        context['my_form'] = form
        return context

    # no per-day limit because you can only rate listings you've been sold to
    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(CreateRating, self).post(request, *args, **kwargs)


class EditRating(LoginRequiredMixin, UpdateView):
    model = Rating
    template_name = 'rating_edit.html'
    context_object_name = 'rating'
    #form_class = EditListingForm
    login_url = 'login'

    fields = ['stars', 'review', ]

    template_suffix_name = '_edit'

    def get_success_url(self):
        return reverse('ratings',
                       kwargs={'slug': self.object.listing.seller.slug})

    def get_context_data(self, **kwargs):
        context = super(EditRating, self).get_context_data(**kwargs)

        me = Student.objects.get(user=self.request.user)
        rating_student = self.get_object().rater

        if not(rating_student == me):
            return HttpResponseForbidden()

        return context


class DeleteRating(LoginRequiredMixin, DeleteView):
    model = Rating
    context_object_name = 'rating'
    template_name = 'delete_rating.html'
    login_url = 'login'

    def get_success_url(self):
        return reverse('detail_listing',
                       kwargs={'slug': self.object.listing.slug})

    def get_context_data(self, **kwargs):
        context = super(DeleteRating, self).get_context_data(**kwargs)

        me = Student.objects.get(user=self.request.user)
        rating_student = self.get_object().rater

        if not(rating_student == me):
            return HttpResponseForbidden()

        return context
