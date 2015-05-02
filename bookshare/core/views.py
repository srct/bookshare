# core django imports
from django.views.generic import DetailView, FormView
from django.core.urlresolvers import reverse
# third-party imports
from braces.views import LoginRequiredMixin
from django.db.models import Sum
from ratelimit.decorators import ratelimit
# imports from your apps
from .models import Student
from .forms import UserNameForm
from lookouts.models import Lookout
from trades.models import Listing, Bid, Rating


class DetailStudent(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'profile.html'
    context_object_name = 'student'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(DetailStudent, self).get_context_data(**kwargs)

        student_listings = Listing.objects.filter(poster=self.get_object().pk)

        total_exchanges = student_listings.filter(exchanged=True).count()

        total_proceeds = Bid.objects.filter(listing__poster__user=self.get_object()).filter(listing__exchanged=True).aggregate(Sum('price'))['price__sum']

        student_ratings = Rating.objects.filter(listing__poster=self.get_object())
        if student_ratings:
            student_stars = [int(rating.stars) for rating in student_ratings]
            print student_stars
            average_stars = sum(student_stars)/float((len(student_stars)))
        else:
            average_stars = None

        context['avg_stars'] = average_stars
        context['listings'] = student_listings
        context['lookouts'] = Lookout.objects.filter(owner=self.get_object())

        context['proceeds'] = total_proceeds
        context['exchanges'] = total_exchanges

        context['bids'] = Bid.objects.filter(bidder=self.get_object())

        return context


class UpdateStudent(LoginRequiredMixin, FormView):
    template_name = 'update_student.html'
    form_class = UserNameForm
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(UpdateStudent, self).get_context_data(**kwargs)

        form = UserNameForm()

        form.fields['first_name'].initial = self.request.user.first_name
        form.fields['last_name'].initial = self.request.user.last_name

        context['form'] = form
        return context

    def form_valid(self, form):
        self.request.user.first_name = form.instance.first_name
        self.request.user.last_name = form.instance.last_name
        self.request.user.save()
        return super(UpdateStudent, self).form_valid(form)

    @ratelimit(key='user', rate='5/m', method='POST', block=True)
    @ratelimit(key='user', rate='10/day', method='POST', block=True)
    def post(self, request, *args, **kwargs):
        return super(UpdateStudent, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profile',
                        kwargs={'slug': self.request.user.student.slug})

class StudentRatings(LoginRequiredMixin, DetailView):
    model = Student
    template_name = 'ratings.html'
    context_object_name = 'student'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super(StudentRatings, self).get_context_data(**kwargs)

        student_ratings = Rating.objects.filter(listing__poster=self.get_object())

        # copied code!
        if student_ratings:
            student_stars = [int(rating.stars) for rating in student_ratings]
            print student_stars
            average_stars = sum(student_stars)/float((len(student_stars)))
        else:
            average_stars = None

        context['avg_stars'] = average_stars

        context['student_ratings'] = student_ratings
        context['student_ratings_num'] = student_ratings.count()

        return context
