from django.conf.urls import patterns, include, url

from lookouts.views import DetailLookout, CreateLookout, DeleteLookout
from lookouts.models import Lookout

urlpatterns = patterns('',

    url(r'^new/$',
        CreateLookout.as_view(
            model=Lookout,
            template_name='create_lookout.html'),
    name='create_lookout'),

    url(r'^(?P<slug>[\w-]+)/$',
        DetailLookout.as_view(
            model=Lookout,
            context_object_name='lookout',
            template_name='detail_lookout.html'),
    name='detail_lookout'),

    url(r'^(?P<slug>[\w-]+)/delete/$',
        DeleteLookout.as_view(
            model=Lookout,
            context_object_name='lookout',
            template_name='delete_lookout.html'),
    name='delete_lookout'),
        
)
