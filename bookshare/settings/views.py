from lookouts.models import Lookout

from django.views.generic import TemplateView

class HomepageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['my_lookouts'] = Lookout.objects.all()
        return context
