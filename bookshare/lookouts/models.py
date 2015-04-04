from django.db import models
from trades.models import Listing
from core.models import Student, Course
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from model_utils.models import TimeStampedModel
from randomslugfield import RandomSlugField

class Lookout(TimeStampedModel):
    owner = models.ForeignKey(Student)
    isbn = models.CharField(
        max_length = 20,
        validators = [RegexValidator('[0-9xX-]{10,20}', message = 'Please enter a valid ISBN.')])
    # would have to load in every conceivable course first
    #course = models.ForeignKey(Course)
    slug = RandomSlugField(length = 6)
    def get_listings(self):
        # may be reason to resurrect active as an actual field, possibly can call function?
        isbn_listings = models.Q( isbn = self.isbn, sold = False, cancelled = False )
        return Listing.objects.filter( isbn_listings )

    # needs get_absolute_url
    def get_absolute_url(self):
        return reverse('detail_lookout', kwargs = {'slug':self.slug})

    def __unicode__(self):
        return '%s %s' % (self.owner.user.username, self.isbn)

    class Meta:
        ordering = ['isbn']
        unique_together = ['owner', 'isbn']
