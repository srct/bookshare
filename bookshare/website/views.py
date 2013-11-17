# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404

# home page
def index(request):
    return render_to_response('index.html', {
    },
    )

# product page
    return render_to_response('product.html', {
    },
    )
