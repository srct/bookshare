# standard library imports
from datetime import date
from io import StringIO
# core django imports
from django.views.generic import View, DetailView, ListView, CreateView,\
    UpdateView, DeleteView
from django.http import Http404, HttpResponseForbidden
from django.forms.widgets import HiddenInput
from django.urls import reverse, reverse_lazy
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.utils.safestring import mark_safe
# third party imports
from PIL import Image
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from braces.views import FormValidMessageMixin
from ratelimit.decorators import ratelimit
# imports from your apps
from .models import Listing, Bid, Flag, BidFlag, Rating
from .forms import ListingForm, BidForm, FlagForm, BidFlagForm,\
                   ExchangeListingForm, UnExchangeListingForm, RatingForm
from .utils import ISBNMetadata, can_flag, can_flag_bid, flag_slug,\
                   bid_flag_slug, can_rate
from core.models import Student


class ListListings(LoginRequiredMixin, ListView):
    model = Listing
    context_object_name = 'listings'
    paginate_by = 16
    queryset = Listing.objects.exclude(cancelled=True).order_by('-created')
    template_name = 'list_listings.html'
    login_url = 'login'


class CreateListing(LoginRequiredMixin, FormValidMessageMixin, CreateView):
    model = Listing
    template_name = 'create_listing.html'
    form_class = ListingForm
    # ISBN query!
    login_url = 'login'
    # eventually figure out how to use {% url 'create_listing' %}
    form_valid_message = mark_safe("""Your listing was successfully created!
                         <a href="/share/new/">Create another here!</a>""")

    def form_valid(self, form):
        me = self.request.user.student

        # you will see this throughout-- this field is not exposed to the user
        # and is instead handled here
        form.instance.poster = me

        # take uploaded image and scale it down before storing
        image_name = form.instance.photo.name
        user_image = Image.open(form.instance.photo)
        image_format = user_image.format

        print(user_image)
        width, height = user_image.size
        print(user_image.size)
        print(width, "width")
        print(height, "height")
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

    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    @ratelimit(key='user', rate='50/day', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(CreateListing, self).post(request, *args, **kwargs)


class DeleteListing(LoginRequiredMixin, SuperuserRequiredMixin, FormValidMessageMixin, DeleteView):
    model = Listing
    template_name = 'delete_listing.html'
    form_valid_message = "The listing was successfully deleted."
    login_url = 'login'
    success_url = reverse_lazy('flag_mod')


# These next three views are tied together...
class DetailListing(LoginRequiredMixin, DetailView):
    model = Listing
    template_name = 'detail_listing.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(DetailListing, self).get_context_data(**kwargs)
        me = self.request.user.student
        self.obj = self.get_object()

        # make the form available to the template on get
        # set the bidder and the listing
        form = BidForm(initial={'listing': self.obj})
        form.fields['listing'].widget = HiddenInput()
        context['my_form'] = form

        try:
            context['rating'] = Rating.objects.get(listing=self.obj)
        except:
            context['rating'] = False

        # bids, filter by listing name of the current listing, order by date created
        bids  = Bid.objects.filter(listing=self.obj).order_by('-price')

        bids_with_info = []
        flagged_bids_with_info = []
        for bid in bids:
            flaggable = can_flag_bid(me, bid)
            the_slug = bid_flag_slug(me, bid)
            info_tuple = (bid, (flaggable, the_slug))
            if not bid.too_many_flags():
                bids_with_info.append(info_tuple)
            else:
                flagged_bids_with_info.append(info_tuple)

        context['bids'] = bids_with_info
        context['flagged_bids'] = flagged_bids_with_info
        context['bid_count'] = Bid.objects.filter(listing=self.obj).count()
        # flags
        context['flags'] = Flag.objects.filter(listing=self.obj).order_by('-created')
        context['flag_count'] = Flag.objects.filter(listing=self.obj).count()
        context['can_flag'] = can_flag(me, self.obj)
        context['flag_slug'] = flag_slug(me, self.obj)
        return context


class DetailListingNoAuth(DetailView):
    model = Listing
    template_name = 'detail_listing_no_auth.html'

    def get_context_data(self, **kwargs):
        context = super(DetailListingNoAuth, self).get_context_data(**kwargs)
        self.obj = self.get_object()
        context['flag_count'] = Flag.objects.filter(listing=self.obj).count()
        context['flags'] = Flag.objects.filter(listing=self.obj).order_by('-created')
        return context


class CreateBid(LoginRequiredMixin, CreateView):
    model = Bid
    fields = ['listing', 'price', 'text', ]
    template_name = 'detail_listing.html'
    login_url = 'login'

    def form_valid(self, form):
        me = self.request.user.student

        form.instance.bidder = me
        return super(CreateBid, self).form_valid(form)

    def get_success_url(self):
        return reverse('detail_listing',
                       kwargs={'slug': self.object.listing.slug})


# ...to make this single view
class ListingPage(View):

    # see this page for an explanation
    # https://docs.djangoproject.com/en/1.7/topics/class-based-views/mixins/#an-alternative-better-solution

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            view = DetailListing.as_view()
            return view(request, *args, **kwargs)
        else:
            view = DetailListingNoAuth.as_view()
            return view(request, *args, **kwargs)

    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    # rate limit is higher for bids
    @ratelimit(key='user', rate='100/d', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            view = CreateBid.as_view()
            return view(request, *args, **kwargs)
        # the nonauthenticated version cannot post
        else:
            pass


# and we return to our regularly scheduled programming
class CreateFlag(LoginRequiredMixin, CreateView):
    model = Flag
    template_name = 'create_flag.html'
    form_class = FlagForm
    login_url = 'login'

    def parse_url_for_listing(self, request):
        # there's possibly a better way than url parsing, but here we are
        current_url = request.get_full_path()
        listing_slug = current_url.split('/')[3]
        # [u'', u'share', u'listing', u'C1s3oD', u'flag']
        return Listing.objects.get(slug=listing_slug)

    def get(self, request, *args, **kwargs):
        me = self.request.user.student
        selected_listing = self.parse_url_for_listing(self.request)
        posting_student = selected_listing.poster

        # can only create a flag if you haven't previously created one
        if not can_flag(me, selected_listing):
            # because the page shouldn't exist in this scenario
            raise Http404

        # you can't flag your own listing
        if (posting_student == me):
            return HttpResponseForbidden()
        else:
            return super(CreateFlag, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateFlag, self).get_context_data(**kwargs)

        context['listing'] = self.parse_url_for_listing(self.request)
        return context

    def form_valid(self, form):
        me = self.request.user.student
        selected_listing = self.parse_url_for_listing(self.request)

        form.instance.flagger = me
        form.instance.listing = selected_listing
        return super(CreateFlag, self).form_valid(form)

    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    @ratelimit(key='user', rate='100/d', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(CreateFlag, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('detail_listing',
                       kwargs={'slug': self.object.listing.slug})


class DeleteFlag(LoginRequiredMixin, FormValidMessageMixin, DeleteView):
    model = Flag
    template_name = 'delete_flag.html'
    form_valid_message = "Your flag was successfully deleted."
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        me = self.request.user.student
        flag_student = self.get_object().flagger

        # if you didn't create the flag, you can't delete the flag
        if not(flag_student == me):
            return HttpResponseForbidden()
        else:
            return super(DeleteFlag, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('detail_listing',
                       kwargs={'slug': self.object.listing.slug})


# so much almost replication, but not sure what else to do
class CreateBidFlag(LoginRequiredMixin, CreateView):
    model = BidFlag
    template_name = 'create_bid_flag.html'
    form_class = BidFlagForm
    context_object_name = 'bidflag'
    login_url = 'login'

    def parse_url_for_bid(self, request):
        # there's possibly a better way than url parsing, but here we are
        current_url = request.get_full_path()
        bid_slug = current_url.split('/')[5]
        # [u'', u'share', u'listing', u'C1s3oD', u'bid', 'u'F17jal', u'flag']
        return Bid.objects.get(slug=bid_slug)

    def get(self, request, *args, **kwargs):
        me = self.request.user.student
        selected_bid = self.parse_url_for_bid(self.request)
        bidding_student = selected_bid.bidder

        # can only create a flag if you haven't previously created one
        if not can_flag_bid(me, selected_bid):
            # because the page shouldn't exist in this scenario
            raise Http404

        # you can't flag your own bid
        if (bidding_student == me):
            return HttpResponseForbidden()
        else:
            return super(CreateBidFlag, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateBidFlag, self).get_context_data(**kwargs)

        context['bid'] = self.parse_url_for_bid(self.request)
        return context

    def form_valid(self, form):
        me = self.request.user.student
        selected_bid = self.parse_url_for_bid(self.request)

        form.instance.flagger = me
        form.instance.bid = selected_bid
        return super(CreateBidFlag, self).form_valid(form)

    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    @ratelimit(key='user', rate='100/d', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(CreateBidFlag, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('detail_listing',
                       kwargs={'slug': self.object.bid.listing.slug})


class DeleteBidFlag(LoginRequiredMixin, FormValidMessageMixin, DeleteView):
    model = BidFlag
    context_object_name = 'bidflag'
    template_name = 'delete_bid_flag.html'
    form_valid_message = "Your flag was successfully deleted."
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        me = self.request.user.student
        flag_student = self.get_object().flagger

        # if you didn't create the flag, you can't delete the flag
        if not(flag_student == me):
            return HttpResponseForbidden()
        else:
            return super(DeleteBidFlag, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('detail_listing',
                       kwargs={'slug': self.object.bid.listing.slug})


# not implemented -- tbd
class DeleteBid(LoginRequiredMixin, DeleteView):
    model = Bid
    success_url = '/'

    # can be deleted by either creator or person for lister


class EditBid(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    model = Bid
    template_name = 'bid_edit.html'
    # form_class = EditBidForm
    fields = ['price', 'text', ]
    login_url = 'login'
    form_valid_message = "Your bid was successfully updated!"

    def get(self, request, *args, **kwargs):
        me = self.request.user.student
        self.obj = self.get_object()
        bidding_student = self.obj.bidder

        # if exchanged or cancelled, this page doesn't exist
        if self.obj.listing.exchanged or self.obj.listing.cancelled:
            raise Http404

        if not(bidding_student == me):
            return HttpResponseForbidden()
        else:
            return super(EditBid, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('detail_listing',
                       kwargs={'slug': self.object.listing.slug})


class EditListing(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    model = Listing
    template_name = 'listing_edit.html'
    # form_class = EditListingForm
    fields = ['title', 'author', 'isbn', 'year', 'edition', 'condition',
              'access_code', 'description', 'price', 'photo', ]
    login_url = 'login'
    form_valid_message = "Your listing was successfully updated!"

    def get(self, request, *args, **kwargs):
        me = self.request.user.student
        self.obj = self.get_object()
        posting_student = self.obj.poster

        # can't edit a bid on a cancelled listing
        if (self.obj.cancelled is True):
            raise Http404

        # can only edit your own bids
        if not(posting_student == me):
            return HttpResponseForbidden()
        else:
            return super(EditListing, self).get(request, *args, **kwargs)


class ExchangeListing(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    model = Listing
    fields = ['email_message', 'winning_bid', ]
    template_name = 'listing_exchange.html'
    login_url = 'login'
    form_valid_message = "Your email was successfully sent!"

    def get(self, request, *args, **kwargs):
        me = self.request.user.student
        self.obj = self.obj
        posting_student = self.obj.poster

        bid_count = Bid.objects.filter(listing=self.obj).count()
        if bid_count < 1:
            # because the page shouldn't exist in this scenario
            raise Http404

        # can't exchange a cancelled listing
        if (self.obj.cancelled is True):
            raise Http404

        # only you can confirm the exchange of your own listing
        if not(posting_student == me):
            return HttpResponseForbidden()
        else:
            return super(ExchangeListing, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ExchangeListing, self).get_context_data(**kwargs)

        form = ExchangeListingForm()
        form.fields['winning_bid'].queryset = Bid.objects.filter(listing=self.get_object())

        context['my_form'] = form

        return context

    def form_valid(self, form):
        # filling out fields
        today = date.today()
        self.obj = self.get_object()

        form.instance.exchanged = True
        form.instance.date_closed = today

        # sending email
        # I'm still second guessing as to whether this should be in this method
        text_email = get_template('email/exchanged.txt')
        html_email = get_template('email/exchanged.html')

        email_context = Context({
            'bidder_first_name': form.instance.winning_bid.bidder.user.first_name,
            'poster_name': self.obj.poster.user.get_full_name(),
            'bid_num': form.instance.winning_bid.price,
            'listing_title': self.obj.title,
            'poster_email': self.obj.poster.user.email,
            'email_message': form.instance.email_message, })

        subject, from_email, to, cc = ('Your bid has been selected on Bookshare!',
                                       'no-reply@bookshare.srct.io',
                                       # form.instance.winning_bid.bidder.user.email,
                                       # self.obj.poster.user.email)
                                       'success@simulator.amazonses.com',
                                       'success@simulator.amazonses.com')
        text_content = text_email.render(email_context)
        html_content = html_email.render(email_context)
        msg = EmailMultiAlternatives(subject, text_content,
                                     from_email, [to], [cc])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        self.obj.poster.emails_sent += 2
        self.obj.poster.save()

        return super(ExchangeListing, self).form_valid(form)

    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    @ratelimit(key='user', rate='50/d', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(ExchangeListing, self).post(request, *args, **kwargs)


class UnExchangeListing(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    model = Listing
    template_name = 'listing_unexchange.html'
    form_class = UnExchangeListingForm
    login_url = 'login'
    form_valid_message = """Your exchange has been successfully cancelled,
                     and your email successfully sent!"""

    def get(self, request, *args, **kwargs):
        me = self.request.user.student
        self.obj = self.get_object()
        posting_student = self.obj.poster

        # you can only cancel the exchange if the listing itself is not cancelled
        if (self.obj.cancelled is True):
            raise Http404

        # only you can cancel the exchange of your own listing
        if not(posting_student == me):
            return HttpResponseForbidden()
        else:
            return super(UnExchangeListing, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.obj = self.get_object()
        text_email = get_template('email/unexchanged.txt')
        html_email = get_template('email/unexchanged.html')

        email_context = Context({
            'bidder_first_name': self.obj.winning_bid.bidder.user.first_name,
            'poster_name': self.obj.poster.user.get_full_name(),
            'bid_num': self.obj.winning_bid.price,
            'listing_title': self.obj.title,
            'poster_email': self.obj.poster.user.email,
            'poster_email': form.instance.email_message, })

        subject, from_email, to, cc = ('Your transaction has been cancelled on Bookshare',
                                       'no-reply@bookshare.srct.io',
                                       # self.obj.winning_bid.bidder.user.email,
                                       # self.obj.poster.user.email)
                                       'success@simulator.amazonses.com',
                                       'success@simulator.amazonses.com')
        text_content = text_email.render(email_context)
        html_content = html_email.render(email_context)
        msg = EmailMultiAlternatives(subject, text_content,
                                     from_email, [to], [cc])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        self.obj.poster.emails_sent += 2
        self.obj.poster.save()

        # this has to come after the email has been sent, otherwise these are
        # cleaned out
        form.instance.exchanged = False
        form.instance.date_closed = None
        form.instance.winning_bid = None

        return super(UnExchangeListing, self).form_valid(form)

    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    @ratelimit(key='user', rate='50/d', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(UnExchangeListing, self).post(request, *args, **kwargs)


class CancelListing(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    model = Listing
    fields = []
    template_name = 'listing_cancel.html'
    login_url = 'login'
    form_valid_message = "Your listing was successfully cancelled!"

    def get(self, request, *args, **kwargs):
        me = self.request.user.student
        self.obj = self.get_object()
        posting_student = self.obj.poster

        # you can only cancel the listing if the listing isn't already cancelled
        if (self.obj.cancelled is True):
            raise Http404

        # only you can cancel your own listing
        if not(posting_student == me):
            return HttpResponseForbidden()
        else:
            return super(CancelListing, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        today = date.today()

        form.instance.cancelled = True
        form.instance.date_closed = today
        return super(CancelListing, self).form_valid(form)


class ReopenListing(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    model = Listing
    fields = []
    template_name = 'listing_reopen.html'
    login_url = 'login'

    form_valid_message = "Your listing was successfully reopened!"

    def get(self, request, *args, **kwargs):
        me = self.request.user.student
        self.obj = self.get_object()
        posting_student = self.obj.poster

        # you can only reopen the listing if the listing is cancelled
        if (self.obj.cancelled is False):
            raise Http404

        # only you can re-open your own listing
        if not(posting_student == me):
            return HttpResponseForbidden()
        else:
            return super(ReopenListing, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.cancelled = False
        form.instance.date_closed = None
        return super(ReopenListing, self).form_valid(form)


class CreateRating(LoginRequiredMixin, CreateView):
    model = Rating
    template_name = 'create_rating.html'
    form_class = RatingForm
    login_url = 'login'

    def parse_url_for_listing(self, request):
        # there's possibly a better way than url parsing, but here we are
        current_url = request.get_full_path()
        listing_slug = current_url.split('/')[3]
        # [u'', u'share', u'listing', u'C1s3oD', u'flag']
        return Listing.objects.get(slug=listing_slug)

    def get(self, request, *args, **kwargs):
        me = self.request.user.student
        selected_listing = self.parse_url_for_listing(self.request)
        winning_student = selected_listing.winning_bid.bidder

        # can only create a rating if you haven't previously created one
        if not can_rate(me, selected_listing):
            # because the page shouldn't exist in this scenario
            raise Http404

        # you can only rate a listing that you won
        if not (winning_student == me):
            return HttpResponseForbidden()
        else:
            return super(CreateRating, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateRating, self).get_context_data(**kwargs)

        context['listing'] = self.parse_url_for_listing(self.request)
        return context

    def form_valid(self, form):
        me = self.request.user.student
        selected_listing = self.parse_url_for_listing(self.request)

        form.instance.rater = me
        form.instance.listing = selected_listing
        return super(CreateRating, self).form_valid(form)

    # no per-day limit because you can only rate listings you've exchanged
    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(CreateRating, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('ratings',
                       kwargs={'slug': self.object.listing.poster.slug})


class EditRating(LoginRequiredMixin, UpdateView):
    model = Rating
    template_name = 'rating_edit.html'
    # form_class = EditListingForm
    login_url = 'login'
    fields = ['stars', 'review', ]

    def get(self, request, *args, **kwargs):
        me = self.request.user.student
        rating_student = self.get_object().rater

        # you can only rate exchanges you're party to
        if not(rating_student == me):
            return HttpResponseForbidden()
        else:
            return super(EditRating, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('ratings',
                       kwargs={'slug': self.object.listing.poster.slug})


class DeleteRating(LoginRequiredMixin, FormValidMessageMixin, DeleteView):
    model = Rating
    template_name = 'delete_rating.html'
    form_valid_message = "Your rating was successfully deleted."
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        me = self.request.user.student
        rating_student = self.get_object().rater

        # you can only delete your own ratings
        if not(rating_student == me):
            return HttpResponseForbidden()
        else:
            return super(DeleteRating, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('detail_listing',
                       kwargs={'slug': self.object.listing.slug})
