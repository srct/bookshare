from lookouts.models import Lookout
from lookouts.forms import LookoutForm

from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from braces.views import LoginRequiredMixin

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

#class UpdateLookout(LoginRequiredMixin, UpdateView):

class DeleteLookout(LoginRequiredMixin, DeleteView):
    model=Lookout
    success_url = '/'
    # user?...
