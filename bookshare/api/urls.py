# core django imports
from django.urls import include, path
# third party imports
from rest_framework.routers import DefaultRouter
# imports from your apps
from .views import ListingViewSet


router = DefaultRouter()

router.register(r'listings', ListingViewSet, 'listing_list')

urlpatterns = router.urls
