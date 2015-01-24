from django.db import models
from trades.models import Listing
from django.conf import settings
from model_utils.models import TimeStampedModel


class Lookout(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    ISBN = models.CharField(max_length = 20)
    # place other possible fields here, ISBN only for right now.

    def __unicode__(self):
        return '<Lookout: %s>' % self.owner.user.username

    def get_listings(self):
        isbn_listings = models.Q( ISBN=self.ISBN, active=True )
        return Listing.objects.filter( isbn_listings )
#        title_listings = models.Q( title=self.title, active=True )
#        return Listing.objects.filter( isbn_listings | title_listings )

    class Meta:
        ordering = ['ISBN']
