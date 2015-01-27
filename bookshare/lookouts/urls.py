from django.conf.urls import patterns, include, url

from lookouts.views import CreateLookout
from lookouts.models import Lookout

urlpatterns = patterns('',

    url(r'^(username)/(?P<slug>[\w-]+)/$',
        CreateLookout.as_view(
        model=Lookout,
        context_object_name='lookout',
        template_name='create_lookout.html'),
    name='create_lookout'),
        

)
