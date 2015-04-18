from django.conf.urls import patterns, url
from core.views import DetailStudent, StudentRatings

urlpatterns = patterns('',
    url(r'^(?P<slug>[\w-]+)/$',
        DetailStudent.as_view(), name='profile'),

    url(r'^(?P<slug>[\w-]+)/ratings/$',
        StudentRatings.as_view(), name='ratings'),
)
