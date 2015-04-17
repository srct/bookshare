from django.views.generic import DetailView
from braces.views import LoginRequiredMixin

from core.models import Student
from lookouts.models import Lookout
from trades.models import Listing, Bid


class DetailStudent(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'profile.html'
    context_object_name = 'student'
    login_url = 'login'

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
