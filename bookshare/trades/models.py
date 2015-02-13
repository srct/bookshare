from django.db import models
from model_utils.models import TimeStampedModel
#from autoslug import AutoSlugField
from randomslugfield import RandomSlugField

from core.models import Course

from django.core.validators import MinValueValidator, RegexValidator
from django.core.urlresolvers import reverse
from django.conf import settings

class Listing(TimeStampedModel):
    NEW = 'New'
    LIKE_NEW = 'Like New'
    VERY_GOOD = 'Very Good'
    GOOD = 'Good'
    ACCEPTABLE = 'Acceptable'
    UNACCEPTABLE = 'Unacceptable'

    BOOK_CONDITION_CHOICES = (
        (NEW, 'New'),
        (LIKE_NEW, 'Like New'),
        (VERY_GOOD, 'Very Good'),
        (GOOD, 'Good'),
        (ACCEPTABLE, 'Acceptable'),
        (UNACCEPTABLE, 'Unacceptable'),
    )

    seller = models.ForeignKey(settings.AUTH_USER_MODEL)

    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 200)
    isbn = models.CharField(
        max_length = 20,
        #validators = [RegexValidator('[0-9xX-]{10,20}', message='Enter a valid ISBN.')]
    )
    year = models.IntegerField(null=True,blank=True)
    edition = models.CharField(blank=True, default=0, max_length = 30)
    # course
    date_sold = models.DateTimeField(null=True,blank=True)
    condition = models.CharField(choices=BOOK_CONDITION_CHOICES,
                                      max_length=20,
                                      default=GOOD)
    description = models.TextField(blank=True)
    #price = models.IntegerField( validators = [MinValueValidator(0)] )
    price = models.IntegerField()
    photo = models.ImageField(
        max_length = 1000,
        upload_to = 'listing_photos',
        default = 'static/img/default_listing_photo.jpg' )

    sold = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    finalPrice = models.IntegerField(blank=True,default=0)

    slug = RandomSlugField(length=6, exclude_upper=True)

    def get_absolute_url(self):
        return reverse('detail_listing', kwargs={'slug':self.slug})

    # retrieve url for object
#    def get_absolute_url(self):
#        from django.core.urlresolvers import reverse
#        return reverse('trades.views.DetailListing', args=[str(self.id)])  

    # object call
    def __unicode__(self):
        if not self.active:
            return '[Inactive] %s : %s' % (self.isbn, self.title)
        return '%s : %s' % (self.isbn, self.title)

    class Meta:
        #unique_together = (("ISBN", "seller"),)
        ordering = ['isbn', 'title']


class Bid(TimeStampedModel):

    bidder = models.ForeignKey(settings.AUTH_USER_MODEL)
    listing = models.ForeignKey(Listing)
    price = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    text = models.CharField( blank=True, max_length = 1000 )

    def __unicode__(self):
        return '%s on %s\'s %s' % (self.bidder,
                                   self.listing.seller,
                                   self.listing)

    class Meta:
        ordering = ['-created']