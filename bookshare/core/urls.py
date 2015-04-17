from django.conf.urls import patterns, url
from core.views import DetailStudent

urlpatterns = patterns('',
    url(r'^(?P<slug>[\w-]+)/$',
        DetailStudent.as_view(), name='profile'),
)
