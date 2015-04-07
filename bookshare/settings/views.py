from lookouts.models import Lookout

from django.views.generic import TemplateView

class HomepageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
          context['lookouts'] = Lookout.objects.filter(owner=self.request.user.student)
        return context
