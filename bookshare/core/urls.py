# core django imports
from django.urls import path
from django.views.decorators.cache import cache_page
# imports from your apps
from .views import DetailStudent, StudentRatings, UpdateStudent

urlpatterns = [
    path('name-change/',
        UpdateStudent.as_view(), name='name_change'),

    path('<slug>/',
        cache_page(6)(DetailStudent.as_view()), name='profile'),

    path('<slug>/ratings/',
        cache_page(6)(StudentRatings.as_view()), name='ratings'),
]
