# core django imports
from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page
# imports from your apps
from .views import DetailLookout, CreateLookout, DeleteLookout

urlpatterns = patterns('',

    url(r'^new/$',
        CreateLookout.as_view(), name='create_lookout'),

    url(r'^(?P<slug>[\w-]+)/$',
        cache_page(60 * 5)(DetailLookout.as_view()), name='detail_lookout'),

    url(r'^(?P<slug>[\w-]+)/delete/$',
        DeleteLookout.as_view(), name='delete_lookout'),
)
