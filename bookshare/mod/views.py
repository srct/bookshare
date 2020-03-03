# core django imports
from django.views.generic import TemplateView, ListView
from django.db.models import Count
# third party imports
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
# imports from your apps
from trades.models import Listing
from core.models import Student


class ModLandingView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = 'mod.html'
    login_url = 'login'

class FlagModView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    queryset = Listing.objects.annotate(num_flags=Count('flag')).order_by('-num_flags')[:20]
    context_object_name = 'listings'
    template_name = 'flag_mod.html'
    login_url = 'login'

class ListingNumModView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    queryset = Student.objects.annotate(num_books=Count('listing')).order_by('-num_books')[:20]
    context_object_name = 'students'
    template_name = 'listing_num_mod.html'
    login_url = 'login'

class UserEmailRatioModView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = 'email_ratio_mod.html'

    def get_context_data(self, **kwargs):
        context = super(UserEmailRatioModView, self).get_context_data(**kwargs)

        students_by_emails = Student.objects.order_by('-emails_sent')[:20]
        students_listings = students_by_emails.annotate(num_books=Count('listing'))

        context['email_happy_students'] = students_listings
        return context
