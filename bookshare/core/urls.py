# core django imports
from django.conf.urls import patterns, url
# imports from your apps
from .views import DetailStudent, StudentRatings, UpdateStudent

urlpatterns = patterns('',
    url(r'^name-change/$',
        UpdateStudent.as_view(), name='name_change'),

    url(r'^(?P<slug>[\w-]+)/$',
        DetailStudent.as_view(), name='profile'),

    url(r'^(?P<slug>[\w-]+)/ratings/$',
        StudentRatings.as_view(), name='ratings'),
)
