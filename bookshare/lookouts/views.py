from lookouts.models import Lookout
from lookouts.forms import LookoutForm

from django.views.generic import CreateView, UpdateView, DeleteView
from braces.views import LoginRequiredMixin


# saved searches
    # need to implement haystack stuff first

### VIEWS ###
class CreateLookout(LoginRequiredMixin, CreateView):
    # can only be viewed by the user who created the lookout!...
    model = Lookout
    form_class = LookoutForm
    success_url = '/'
    login_url = '/'

# remember, see all the lookouts on the homepage

#class UpdateLookout(LoginRequiredMixin, UpdateView):

class DeleteLookout(LoginRequiredMixin, DeleteView):
    model=Lookout
    success_url = '/'
    # user?...
