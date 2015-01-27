from django.shortcuts import render

from django.views.generic import DetailView
from braces.views import LoginRequiredMixin

from core.models import Student

# stuff copied out of the website views

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

# USER home page -- rewrite as user homepage
#@login_required
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

    if request.method == 'POST':
        lookout_form = LookoutForm( request.POST )
        if lookout_form.is_valid():
            lookout = lookout_form.save(commit=False)
            lookout.ISBN = lookout.ISBN.strip()
            lookout.owner = request.user.seller
            lookout.save()
            return redirect( 'homepage' )

    return render(request, 'index.html', {
        'listings' : listings,
        'rows' : rows,
        'CreateLookout_form': lookout_form,
    },
    )

# User profile page
class DetailStudent(LoginRequiredMixin, DetailView):
    model = Student
    login_url = '/'

# user settings page
# manage all listings -- close your listings, delete your listings, see your bids, remove your bids, close your bids, etc

#@login_required
def search(request):
    # merely forms
    return render(request, 'search.html', {
    },
    )
