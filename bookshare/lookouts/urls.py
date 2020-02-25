# core django imports
from django.urls import path
from django.views.decorators.cache import cache_page
# imports from your apps
from .views import DetailLookout, CreateLookout, DeleteLookout

urlpatterns = [

    path('new/',
        CreateLookout.as_view(), name='create_lookout'),

    path('<slug>/',
        cache_page(60 * 2)(DetailLookout.as_view()), name='detail_lookout'),

    path('<slug>/delete/',
        DeleteLookout.as_view(), name='delete_lookout'),
]
