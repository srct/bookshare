# core django imports
from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page
# imports from your apps
from .views import DetailStudent, StudentRatings

urlpatterns = patterns('',
    url(r'^(?P<slug>[\w-]+)/$',
        cache_page(60 * 2)(DetailStudent.as_view()), name='profile'),

    url(r'^(?P<slug>[\w-]+)/ratings/$',
        cache_page(60 * 2)(StudentRatings.as_view()), name='ratings'),
)
