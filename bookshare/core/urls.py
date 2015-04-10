from django.conf.urls import patterns, include, url
from core.views import DetailStudent
from core.models import Student

urlpatterns = patterns('',
    url(r'^(?P<slug>[\w-]+)/$',
        DetailStudent.as_view(), name='profile'),
)
