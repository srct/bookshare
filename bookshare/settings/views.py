# standard library imports
from collections import Counter
# core django imports
from django.views.generic import TemplateView
from django.db.models import Sum, Count
# third party imports
from braces.views import LoginRequiredMixin
# imports from your apps
from lookouts.models import Lookout
from trades.models import Listing, Bid
from core.models import Student


class HomepageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['lookouts'] = Lookout.objects.filter(owner=self.request.user)
        return context


class ChartsView(TemplateView):
    template_name = 'charts.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(ChartsView, self).get_context_data(**kwargs)

        all_listings = Listing.objects.exclude(cancelled=True)

        all_isbns = [listing.isbn for listing in all_listings]

        grossing = []
        # set to eliminate duplicates
        for isbn in set(all_isbns):
            # only want exchanged listings (not cancelled is assumed)
            listings = Listing.objects.exclude(exchanged=False).filter(isbn=isbn)
            # make list of all of that listing's final prices (assume no Nones)
            listing_winning_bids = [listing.final_price() for listing in listings]
            # add all those together
            listing_gross = sum(listing_winning_bids)
            # make a tuple of the isbn and gross and add it to the list
            grossing.append((isbn, listing_gross))

        total_proceeds = Listing.objects.aggregate(sum_price=Sum('winning_bid__price'))['sum_price']

        context['most_popular'] = Counter(all_isbns).most_common(20)
        # sort by the second element of the tuple, descending
        context['highest_grossing'] = sorted(grossing, key=lambda li: li[1],
                                             reverse=True)[:20]
        context['total_listings'] = all_listings.count()
        context['total_bids'] = Bid.objects.count()
        context['total_students'] = Student.objects.count()
        context['total_proceeds'] = total_proceeds
        return context
