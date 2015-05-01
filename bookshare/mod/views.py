# core django imports
from django.views.generic import TemplateView, ListView
from django.db.models import Sum
# third party imports
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
# imports from your apps
from trades.models import Listing


class ModLandingView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = 'mod.html'

class FlagModView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    queryset = Listing.objects.annotate(num_flags=Count('flag')).order_by('-num_flags')[:20]
    context_object_name = 'listings'
    template_name = 'flag_mod.html'
    login_url = 'login'

class ListingNumModView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    queryset = Listing.objects.all()[:20]
    context_object_name = 'users'
    template_name = 'listing_num_mod.html'
    login_url = 'login'

class UserEmailRatioModView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    template_name = 'email_ratio_mod.html'

    def get_context_data(self, **kwargs):
        context = super(UserEmailRatioView, self).get_context_data(**kwargs)
        return context
