from django.db import models
from trades.models import Listing
from core.models import Course
from django.conf import settings
from model_utils.models import TimeStampedModel
from autoslug import AutoSlugField
from randomslugfield import RandomSlugField

class Lookout(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    isbn = models.CharField(max_length = 20)
    #course = models.ForeignKey('Course')
    # place other possible fields here, ISBN and Course only for right now.

    isbnslug = AutoSlugField(populate_from='isbn')
    randomslug = RandomSlugField(length=6, exclude_upper=True)

    # needs get_absolute_url

    # this should change
    def __unicode__(self):
        return '<Lookout: %s>' % self.owner.user.username

    def get_listings(self):
        isbn_listings = models.Q( isbn=self.isbn, active=True )
        return Listing.objects.filter( isbn_listings )
#        title_listings = models.Q( title=self.title, active=True )
#        return Listing.objects.filter( isbn_listings | title_listings )

    class Meta:
        ordering = ['isbn']
