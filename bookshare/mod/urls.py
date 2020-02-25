# core django imports
from django.urls import path
from django.views.decorators.cache import cache_page
# imports from your apps
from .views import ModLandingView, FlagModView, ListingNumModView,\
    UserEmailRatioModView

urlpatterns = [
    path('', cache_page(60 * 15)(ModLandingView.as_view()), name='mod_page'),

    path('flags/', FlagModView.as_view(), name='flag_mod'),

    path('listing-nums/', ListingNumModView.as_view(), name='listing_nums'),

    path('email-ratio/', UserEmailRatioModView.as_view(), name='email_ratio'),

]
