from lookouts.models import Lookout
from trades.models import Listing, Bid
from core.models import Student

from django.views.generic import TemplateView

from collections import Counter

class HomepageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
          context['lookouts'] = Lookout.objects.filter(owner=self.request.user.student)
        return context

class ChartsView(TemplateView):
    template_name = 'charts.html'

    def get_context_data(self, **kwargs):
        context = super(ChartsView, self).get_context_data(**kwargs)

        all_listings = Listing.objects.exclude(cancelled=True)

        all_isbns = [listing.isbn for listing in all_listings]

        grossing = []
        # set to eliminate duplicates
        for isbn in set(all_isbns):
            # only want sold listings (not cancelled is assumed)
            listings = Listing.objects.exclude(sold=False).filter(isbn=isbn)
            # make a list of all of that listing's final prices (assuming no Nones)
            listing_winning_bids = [listing.final_price() for listing in listings]
            # add all those together
            listing_gross = sum(listing_winning_bids)
            # make a tuple of the isbn and gross and add it to the list
            grossing.append( (isbn, listing_gross) )

        context['most_popular'] = Counter(all_isbns).most_common(20)
        # sort by the second element of the tuple, descending
        context['highest_grossing'] = sorted(grossing, key=lambda li: li[1], reverse=True)[:20]
        context['total_listings'] = all_listings.count()
        context['total_bids'] = Bid.objects.count()
        context['total_students'] = Student.objects.count()
        return context
