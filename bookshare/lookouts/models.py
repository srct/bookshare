from django.db import models
from trades.models import Listing
from core.models import Course
from django.conf import settings
from django.core.urlresolvers import reverse
from model_utils.models import TimeStampedModel
from randomslugfield import RandomSlugField

class Lookout(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    isbn = models.CharField(max_length = 20)

    slug = RandomSlugField(length=6, exclude_upper=True)
    def get_listings(self):
        isbn_listings = models.Q( isbn=self.isbn, active=True )
        return Listing.objects.filter( isbn_listings )

    # needs get_absolute_url
    def get_absolute_url(self):
        return reverse('detail_lookout', kwargs={'slug':self.slug})

    def __unicode__(self):
        return '%s %s' % (self.owner.username, self.isbn)

    class Meta:
        ordering = ['isbn']
        unique_together = ['owner', 'isbn']
