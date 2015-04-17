from lookouts.models import Lookout
from lookouts.forms import LookoutForm

from django.views.generic import CreateView, DetailView, DeleteView
from braces.views import LoginRequiredMixin

from core.models import Student
from django.http import HttpResponseForbidden


class CreateLookout(LoginRequiredMixin, CreateView):
    model = Lookout
    fields = ['isbn', ]
    context_object_name = 'lookout'
    template_name = 'create_lookout.html'
    login_url = '/'

    def form_valid(self, form):
        me = Student.objects.get(user=self.request.user)

        form.instance.owner = me
        return super(CreateLookout, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateLookout, self).get_context_data(**kwargs)

        form = LookoutForm()
        context['my_form'] = form

        return context


class DetailLookout(LoginRequiredMixin, DetailView):
    model = Lookout
    context_object_name = 'lookout'
    template_name = 'detail_lookout.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super(DetailLookout, self).get_context_data(**kwargs)

        me = Student.objects.get(user=self.request.user)
        lookout_student = self.get_object().owner

        if not(lookout_student == me):
            return HttpResponseForbidden()

        return context

# updating is not neccessary since it's just literally an isbn and a course


class DeleteLookout(LoginRequiredMixin, DeleteView):
    model = Lookout
    context_object_name = 'lookout'
    template_name = 'delete_lookout.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(DeleteLookout, self).get_context_data(**kwargs)

        me = Student.objects.get(user=self.request.user)
        lookout_student = self.get_object().owner

        if not(lookout_student == me):
            return HttpResponseForbidden()

        return context
