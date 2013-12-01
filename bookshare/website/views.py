from website.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage

# home page
def index(request):

#    # front page of the site shows the 12 most recent listings
#    products = Book.objects.all().order_by("-uploaded")
#    paginator = Paginator(products, 12)
#
#    # can we get a first page please?
#    try:
#        page = int(request.GET.get("page", '1'))
#    except ValueError: page = 1
#
#    # how many pages do we have?
#    try:
#        products = paginator.page(page)
#    except (InvalidPage, EmptyPage):
#        blogs = paginator.page(paginator.num_pages)
    
    # need to figure out what needs to be displayed/accessed

    # ability to create and display saved searches
    # pull all comments from listings user has posted on and their listings
    # make pagination work
    # NEED TO HAVE THE SEARCH WORK--- YAY HAYSTACK
    return render_to_response('index.html', {

    },
    )

# User profile page
def profile(request, slug):
    return render_to_response('profile.html', {
        'seller': get_object_or_404(Seller, username=slug),
    },
    )

# User listings page
def user_listings(request, slug):
    return render_to_response('user_listings.html', {
        'listings': Listing.objects.filter(seller__username=slug),
    },
    )

# Listing page
def listing(request, slug, book_slug):
    # functions--
    # bidding ranking
    # customized commenting
    # if enters bid, comment
    # IF lister, different things in the template appear
    return render_to_response('listing.html', {
        'listing' : get_object_or_404(Listing,pk=book_slug),
    },
    )

def create_listing(request):
    # merely forms
    return render_to_response('create_listing.html', {
    
    },
    )
