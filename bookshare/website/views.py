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

# product page
def listing(request, slug):
    # functions--
    # bidding ranking
    # customized commenting
    # if enters bid, comment
    # IF lister, different things in the template appear

    return render_to_response('listing.html', {
        'listing': get_object_or_404(Book, slug=slug),
    },
    )

def create_listing(request):
    # merely forms
    return render_to_response('create_listing.html', {
    
    },
    )

def my_listings(request):
    # get all listings from user, sorted by time
    return render_to_response('my_listings.html', {
        'listings' : Listing.objects.all(),
    },
    )

def seller_profile(request):
    # retrieve user object
    # IF the seller, different things in the templates appear
    return render_to_response('seller_profile', {

    },
    )

def my_profile(request):
    # retrieve user object
    # IF the seller, different things in the templates appear
    return render_to_response('seller_profile', {

    },
    )
