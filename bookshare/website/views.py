# Create your views here.

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
    return render_to_response('index.html', {
        # titles
        # ISBN
    },
    )

# product page
def listing(request, slug):
    
    return render_to_response('listing.html', {
        'listing': get_object_or_404(Book, slug=slug),
    },
    )

def create_listing(request):

    return render_to_response('create_listing.html', {
    
    },
    )

def my_listings(request):

    return render_to_response('my_listings.html', {

    },
    )

def seller_profile(request):

    return render_to_response('seller_profile', {

    },
    )
