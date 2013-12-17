from django.db import models
from django.utils import timezone
from website.models import Seller, Listing

# Create your models here.
class Lookout( models.Model ):

    owner = models.ForeignKey(Seller)
    date_created = models.DateTimeField(default=timezone.now())

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
