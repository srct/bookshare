from lookouts.models import Lookout
from lookouts.forms import LookoutForm

from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from braces.views import LoginRequiredMixin

from django.contrib.auth.models import User
from django.http import Http404

### VIEWS ###
class CreateLookout(LoginRequiredMixin, CreateView):
    # can only be viewed by the user who created the lookout!...
    model = Lookout
    form_class = LookoutForm
#    success_url = '/'
# should redirect to get_absolute_url
    login_url = '/'

class DetailLookout(LoginRequiredMixin, DetailView):
    model = Lookout
    context_object_name = 'lookout'
    login_url = '/'

# remember, see all the lookouts on the homepage

# updating is not neccessary since it's just literally an isbn and a course

class DeleteLookout(LoginRequiredMixin, DeleteView):
    model=Lookout
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(DeleteLookout, self).get_context_data(**kwargs)

        requesting_student = User.objects.get(username=self.request.user.username)
        lookout_student = self.get_object().owner.user

        if not(requesting_student == lookout_student):
            raise Http404

        return context
