from django.shortcuts import render

from django.views.generic import DetailView
from braces.views import LoginRequiredMixin

from core.models import Student
from lookouts.models import Lookout
from trades.models import Listing

# seller's rating
"""def ratingsAverage(seller):
    sellerRating = Seller.objects.filter(user__username=seller)
    ratingNumber = 0
    ratingTotal = 0
    ratingAverage = 0
    for rating in sellerRating:
        ratingNumber += 1
        ratingTotal += rating
    ratingAverage = ratingTotal/ratingNumber
    return ratingNumber"""

### VIEWS ###

def privacy_opt_out(request):
    # merely forms
    return render(request, 'privacy_opt_out.html', {
   },
   )

def index(request):

    lookout_form = LookoutForm()
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
        'CreateLookout_form': lookout_form,
    },
    )

# User profile page
class DetailStudent(LoginRequiredMixin, DetailView):
    model = Student

    def get_context_data(self, **kwargs):

        def total_sales(listings):
            sales = 0
            for listing in listings:
                if listing.sold:
                    sales = sales + 1
            return sales

        def total_proceeds(listings):
            proceeds = 0
            for listing in listings:
                if listing.sold:
                    proceeds = proceeds + listing.finalPrice
            return proceeds

        student_listings = Listing.objects.filter(seller=self.get_object().pk)

        context = super(DetailStudent, self).get_context_data(**kwargs)

        #context['listings'] = Listing.objects.filter(seller='2')
        context['listings'] = student_listings
        context['me'] = self.get_object().pk
        context['lookouts'] = Lookout.objects.filter(owner=self.get_object().user)

        context['proceeds'] = total_proceeds(student_listings)
        context['sales'] = total_sales(student_listings)

        return context

    login_url = '/'

# manage all listings -- close your listings, delete your listings, see your bids, remove your bids, close your bids, etc -- on both sides of the transactions, and the ratings
# other students see all of your previous transactions but without the editing options ofc
