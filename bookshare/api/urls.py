# standard libary imports
from __future__ import absolute_import, print_function, unicode_literals
# core django imports
from django.conf.urls import include, url
# third party imports
from rest_framework.routers import DefaultRouter
# imports from your apps
from .views import ListingViewSet


router = DefaultRouter()

router.register(r'listings', ListingViewSet, 'listing_list')

urlpatterns = router.urls
