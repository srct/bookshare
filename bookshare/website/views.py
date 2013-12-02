from website.models import Listing,Seller
from django.http import Http404
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime import datetime, timedelta

import pyisbn
import requests

# pulls worldcat metadata from ISBNs
def ISBNMetadata(standardISBN):
    url = "http://xisbn.worldcat.org/webservices/xid/isbn/" + standardISBN + "?method=getMetadata&format=json&fl=title,year,author,ed"
    metadata = request.get(url)
    # format into a dictionary
    dejson = metadata.json()
    metadataDict = dejson['list'][0]
    return metadataDict

# gamification
def totalSold(seller):
    soldList = Listing.objects.filter(seller__username=seller)
    totalSold = 0
    for book in soldList:
        if book.finalPrice:
            totalSold += book.finalPrice
    return totalSold

# validation of new listing forms

# relevant comments

def relevantComments(seller):
    sellerListings = Listing.objects.filter(seller__username=seller).order_by("-date_created")
    # all listings that seller has commented on (preferably ordered in reverse)
    # put those lists together
    # return that list
    return False

# saved searches

# seller's rating

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

    # verify that the user exists
    seller = get_object_or_404(Seller, username=slug)
    listings = Listing.objects.filter(seller__username=slug)

    return render_to_response('profile.html', {
        'seller' : seller,
        'listings': listings,
        'total_sold' : totalSold( slug ),
    },
    )

# User listings page
def user_listings(request, slug):

    # verify that the user exists
    seller = get_object_or_404(Seller, username=slug)
    listings = Listing.objects.filter(seller__username=slug)

    return render_to_response('user_listings.html', {
        'seller' : seller,
        'listings': listings,
    },
    )

# Listing page
def listing(request, slug, book_slug):

    seller = get_object_or_404(Seller,username=slug)
    listing = get_object_or_404(Listing,pk=book_slug)

    # if the listing is over a week old, it's old
    old_threshold = datetime.now() - timedelta(weeks=3)

    # make a thumbnail of the image
#    from PIL import Image
#    size = (100, 100)
#    image = Image.open( listing.photo )
#    image.thumbnail(size, Image.ANTIALIAS)
#    background = Image.new('RGBA', size, (255, 255, 255, 0))
#    background.paste( image,
#        ((size[0] - image.size[0]) / 2, (size[1] - image.size[1]) / 2))

    if listing.seller != seller:
        raise Http404("Seller does not match listing.")

    return render_to_response('listing.html', {
        'listing' : listing,
        'media' : settings.MEDIA_URL,
        'old' : listing.date_created < old_threshold,
#        'thumbnail' : background,
    },
    )

def create_listing(request):
    # merely forms
    return render_to_response('create_listing.html', {
    
    },
    )

def search(request):
    # merely forms
    return render_to_response('search.html', {
    
    },
    )

def about(request):
    # merely forms
    return render_to_response('about.html', {
    },
    )

def contact(request):
    # merely forms
    return render_to_response('contact.html', {
    },
    )

def privacy(request):
    # merely forms
    return render_to_response('privacy.html', {
    },
    )

#def security(request):
#    # merely forms
#    return render_to_response('security.html', {
#    },
#    )
