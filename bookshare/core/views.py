from django.views.generic import DetailView
from braces.views import LoginRequiredMixin

from core.models import Student
from lookouts.models import Lookout
from trades.models import Listing, Bid

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

# User profile page
class DetailStudent(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'profile.html'
    context_object_name = 'student'

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
                    try:
                        proceeds = proceeds + listing.final_price()
                    except:
                        pass
            return proceeds

        student_listings = Listing.objects.filter(seller=self.get_object().pk)

        context = super(DetailStudent, self).get_context_data(**kwargs)

        #context['listings'] = Listing.objects.filter(seller='2')
        context['listings'] = student_listings
        context['me'] = self.get_object().pk
        context['lookouts'] = Lookout.objects.filter(owner=self.get_object())

        context['proceeds'] = total_proceeds(student_listings)
        context['sales'] = total_sales(student_listings)

        context['bids'] = Bid.objects.filter(bidder=self.get_object())

        return context

    login_url = '/'

# manage all listings -- close your listings, delete your listings, see your bids, remove your bids, close your bids, etc -- on both sides of the transactions, and the ratings
# other students see all of your previous transactions but without the editing options ofc
