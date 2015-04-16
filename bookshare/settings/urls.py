from django.conf.urls import patterns, include, url

from .views import HomepageView, ChartsView
from django.views.generic import TemplateView

from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin

# Uncomment the next two lines to enable the admin:
admin.autodiscover()

handle404 = TemplateView.as_view(template_name="404.html")
handle500 = TemplateView.as_view(template_name="500.html")

urlpatterns = patterns('',

    # app-level urls
    url(r'^share/', include('trades.urls')),
    url(r'^student/', include('core.urls')),
    url(r'^lookouts/', include('lookouts.urls')),

    # search
    url(r'^search/', include('haystack.urls'), name='search'),

    # site-wide pages
    url(r'^$', HomepageView.as_view(), name = 'homepage'),
    url(r'^charts/?$', ChartsView.as_view(), name = 'charts'),

    ### static pages ###
    url(r'^about/?$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^privacy/?$', TemplateView.as_view(template_name='privacy.html'), name='privacy'),
    url(r'^privacy/opt-out/?$', 'core.views.privacy_opt_out', name='privacy_opt_out'),

    ### user authentication ###
    url(r'^login/$', 'cas.views.login', name='login'),
    url(r'^logout/$', 'cas.views.logout', name='logout'),

    #### admin pages ####
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
