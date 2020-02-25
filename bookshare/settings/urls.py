# core django imports
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
# third party imports
from haystack.views import SearchView
from cas.views import login, logout
# imports from your apps
from .views import HomepageView, ChartsView
from trades.forms import ListingSearchForm


admin.autodiscover()

handle403 = TemplateView.as_view(template_name="403.html")
handle404 = TemplateView.as_view(template_name="404.html")
handle500 = TemplateView.as_view(template_name="500.html")

urlpatterns = [
    # app-level urls
    path('share/', include('trades.urls')),
    path('student/', include('core.urls')),
    path('lookouts/', include('lookouts.urls')),
    path('mod/', include('mod.urls')),

    # search
    path('search/', login_required(SearchView(form_class=ListingSearchForm),
                                   login_url='login'), name='search'),

    # site-wide pages
    # homepage is weird for cacheing... no special url, but different content
    # for each user
    path('', HomepageView.as_view(), name='homepage'),
    path('charts/', ChartsView.as_view(), name='charts'),

    # static pages
    path('about/',
        cache_page(60 * 15)(TemplateView.as_view(template_name='about.html')),
        name='about'),
    path('privacy/',
        cache_page(60 * 15)(TemplateView.as_view(template_name='privacy.html')),
        name='privacy'),

    # user authentication
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),

    # admin pages
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),

    # api
    path('api/v1/', include('api.urls')),
    # establishing versioning already so we easily can move to another API release
    # without specific version redirects to latest version
    path('api/', RedirectView.as_view(url="v1/")),

    # location of user-uploaded media files from settings.py (for local)
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
