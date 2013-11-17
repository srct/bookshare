# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404

from django.core.paginator import Paginator, InvalidPage, EmptyPage

# home page
def index(request):

    # front page of the site shows the 12 most recent listings
    products = Books.objects.all().order_by("-uploaded")
    paginator = Paginator(products, 12)

    # can we get a first page please?
    try:
        page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    # how many pages do we have?
    try:
        products = paginator.page(page)
    except (InvalidPage, EmptyPage):
        blogs = paginator.page(paginator.num_pages)
    
    # need to figure out what needs to be displayed/accessed
    return render_to_response('index.html', {
        # titles
        # ISBN
    },
    )

# product page
def product(request):
    return render_to_response('product.html', {
    },
    )
