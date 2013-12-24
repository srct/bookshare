from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from website.models import Seller, Listing

# Create your models here.
class Bid( models.Model ):

    bidder = models.ForeignKey(Seller)
    listing = models.ForeignKey(Listing)
    date_created = models.DateTimeField( default=timezone.now() )

    price = models.IntegerField( validators=[MinValueValidator(0)] )
    text = models.CharField( blank=True, max_length = 1000 )

    def __unicode__(self):
        return '%s on %s\'s %s' % (self.bidder,
                                   self.listing.seller,
                                   self.listing)

    class Meta:
        ordering = ['-date_created']
