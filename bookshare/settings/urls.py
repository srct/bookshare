# core django imports
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.decorators.cache import cache_page
# imports from your apps
from .views import HomepageView, ChartsView


admin.autodiscover()

handle403 = TemplateView.as_view(template_name="403.html")
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
    # this page is weird for cacheing... no special url, but different content
    # for each user
    url(r'^$', HomepageView.as_view(), name='homepage'),
    url(r'^charts/?$', cache_page(60 * 10)(ChartsView.as_view()), name='charts'),

    # static pages
    url(r'^about/?$',
        cache_page(60 * 15)(TemplateView.as_view(template_name='about.html')),
        name='about'),
    url(r'^privacy/?$',
        cache_page(60 * 15)(TemplateView.as_view(template_name='privacy.html')),
        name='privacy'),

    # user authentication
    url(r'^login/$', 'cas.views.login', name='login'),
    url(r'^logout/$', 'cas.views.logout', name='logout'),

    # admin pages
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # location of user-uploaded media files from settings.py (for local)
) #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
