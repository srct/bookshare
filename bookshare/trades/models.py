from django.db import models
from model_utils.models import TimeStampedModel
#from autoslug import AutoSlugField
from randomslugfield import RandomSlugField

from core.models import Student, Course

from django.core.validators import MaxValueValidator, RegexValidator
from django.core.urlresolvers import reverse
from django.conf import settings

from datetime import date
from dateutil.relativedelta import relativedelta

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

    seller = models.ForeignKey(Student)

    title = models.CharField(
        max_length = 200)
    author = models.CharField(
        max_length = 200)
    isbn = models.CharField(
        max_length = 20,
        validators = [RegexValidator('[0-9xX-]{10,20}', message = 'Please enter a valid ISBN.')])
    year = models.IntegerField(
        null = True,
        blank = True,
        # some professors may assign books still to be officially published
        validators = [MaxValueValidator(date.today().year+1)])
    edition = models.PositiveIntegerField(
        blank = True,
        default = 1,
        validators = [MaxValueValidator(1000)])
    # would have to load in every conceivable course first
    #course = models.ForeignKey(Course)
    condition = models.CharField(choices = BOOK_CONDITION_CHOICES,
        max_length = 20,
        default = GOOD)
    description = models.TextField(
        blank = True,
        max_length = 2000)
    price = models.PositiveIntegerField(
        default = 0,
        validators = [MaxValueValidator(1000)])
    photo = models.ImageField(
        max_length = 1000,
        upload_to = 'listing_photos',
        default = 'static/img/default_listing_photo.jpg' )

    # these remaining fields are for internal usage, not for users
    sold = models.BooleanField(default = False)
    cancelled = models.BooleanField(default = False)

    email_message = models.TextField(
        blank = True,
        max_length = 2000)

    # future feature: tell sellers what price their book has been getting
    winning_bid = models.ForeignKey('Bid',
        blank=True, null=True, related_name='winning_bid')
    # the date either cancelled or sold
    date_closed = models.DateField(null = True, blank = True)

    slug = RandomSlugField(length = 6)

    def active(self):
        today = date.today()
        # listing last created/modified + a month
        created_plus_month = self.created.date() + relativedelta(months = 1)
        modified_plus_month = self.modified.date() + relativedelta(months = 1)

        # last login + two weeks
        last_login_plus_two_weeks = self.seller.last_login.date() + relativedelta(weeks = 2)

        last_poked = ((today > created_plus_month) or (today > modified_plus_month))
        recent_login = (today > last_login_plus_two_weeks)

        if last_poked and recent_login:
            return False
        else:
            return True

    def final_price(self):
        try:
            price = self.winning_bid.price
        except:
            price = None
        return price

    # retrieve url for object
    def get_absolute_url(self):
        return reverse('detail_listing', kwargs = {'slug':self.slug})

    # object call
    def __unicode__(self):
        return '%s : %s' % (self.isbn, self.title)

    class Meta:
        #unique_together = (("ISBN", "seller"),)
        ordering = ['isbn', 'title']

class Bid(TimeStampedModel):

    bidder = models.ForeignKey(Student)
    listing = models.ForeignKey(Listing)
    price = models.PositiveIntegerField(
        validators = [MaxValueValidator(1000)],)
    text = models.CharField(
        blank = True,
        max_length = 2000,)

    def __unicode__(self):
        return '%s\'s bid for $%s' % (self.bidder,
                             str(self.price))

    class Meta:
        ordering = ['-created']
