# core django imports
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.db import IntegrityError
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, DetailView, DeleteView
# third-party imports
from braces.views import LoginRequiredMixin, FormValidMessageMixin
from ratelimit.decorators import ratelimit
# imports from your apps
from .forms import LookoutForm
from .models import Lookout
from core.models import Student


class CreateLookout(LoginRequiredMixin, CreateView):
    model = Lookout
    form_class = LookoutForm
    context_object_name = 'lookout'
    template_name = 'create_lookout.html'
    login_url = 'login'

    def form_valid(self, form):
        me = self.request.user.student

        form.instance.owner = me
        try:
            return super(CreateLookout, self).form_valid(form)
        except IntegrityError:
            preexisting_lookout = Lookout.objects.get(owner=form.instance.owner, isbn=form.instance.isbn)
            link_lookout = '<a href="/lookouts/%s/">' % (preexisting_lookout.slug)
            integrity_msg = mark_safe("""You already have a lookout for that ISBN!
                                         %sSee it here.</a>""" % (link_lookout))
            messages.add_message(self.request, messages.INFO, integrity_msg)
            return HttpResponseRedirect(reverse('create_lookout'))

    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    @ratelimit(key='user', rate='50/d', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(CreateLookout, self).post(request, *args, **kwargs)

class DetailLookout(LoginRequiredMixin, DetailView):
    model = Lookout
    context_object_name = 'lookout'
    template_name = 'detail_lookout.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        me = self.request.user.student
        lookout_student = self.get_object().owner

        if not(lookout_student == me):
            return HttpResponseForbidden()

        return super(DetailLookout, self).get(request, *args, **kwargs)

# updating is not neccessary since it's just literally an isbn and a course


class DeleteLookout(LoginRequiredMixin, FormValidMessageMixin, DeleteView):
    model = Lookout
    context_object_name = 'lookout'
    template_name = 'delete_lookout.html'
    success_url = '/'
    login_url = 'login'

    form_valid_message = "Your lookout was successfully deleted."

    def get(self, request, *args, **kwargs):
        me = self.request.user.student
        lookout_student = self.get_object().owner

        if not(lookout_student == me):
            return HttpResponseForbidden()

        return super(DeleteLookout, self).get(request, *args, **kwargs)
