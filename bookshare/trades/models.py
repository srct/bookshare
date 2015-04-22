# standard library imports
from datetime import date
# core django imports
from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, RegexValidator
# third party imports
from randomslugfield import RandomSlugField
from model_utils.models import TimeStampedModel
from dateutil.relativedelta import relativedelta
# imports from your apps
from core.models import Student  # and later, Course


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

    NOT_APPLICABLE = 'Not Applicable'
    AC_INCLUDED = 'Access Code Included'
    AC_NOT_INCLUDED = 'Access Code NOT Included'

    ACCESS_CODE_CHOICES = (
        (NOT_APPLICABLE, 'Not Applicable'),
        (AC_INCLUDED, 'Access Code Included'),
        (AC_NOT_INCLUDED, 'Access Code NOT Included'),
    )

    poster = models.ForeignKey(Student)

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20,
                            validators=[RegexValidator('^[0-9xX-]{10,20}',
                                        message='Please enter a valid ISBN.')])
    year = models.IntegerField(null=True, blank=True,
        # some professors may assign books still to be officially published
        validators=[MaxValueValidator(date.today().year+1)])
    edition = models.PositiveIntegerField(null=True, blank=True, default=1,
        validators=[MaxValueValidator(1000)])
    # would have to load in every conceivable course first
    # course = models.ForeignKey(Course)
    condition = models.CharField(choices=BOOK_CONDITION_CHOICES,
                                 max_length=20, default=GOOD)
    access_code = models.CharField(choices=ACCESS_CODE_CHOICES,
                                   max_length=30, default=NOT_APPLICABLE)
    course_abbr = models.CharField(max_length=10, blank=True,
                                   validators=[RegexValidator('^([a-zA-Z]){2,4} (\d){3}$',
                                               message='Please enter a valid course.')])
    description = models.TextField(blank=True, max_length=2000)
    price = models.PositiveIntegerField(default=0,
                                        validators=[MaxValueValidator(1000)])
    photo = models.ImageField(max_length=1000, upload_to='listing_photos',
                              default='listing_photos/default_listing_photo.jpg')

    # these remaining fields are for internal usage, not for users
    exchanged = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)

    email_message = models.TextField(blank=True, max_length=2000)

    # future feature: tell posters what price their book has been getting
    winning_bid = models.ForeignKey('Bid', blank=True, null=True,
                                    related_name='winning_bid')
    # the date either cancelled or exchanged
    date_closed = models.DateField(null=True, blank=True)

    slug = RandomSlugField(length=6)

    def active(self):
        today = date.today()
        # listing last created/modified + a month
        created_plus_month = self.created.date() + relativedelta(months=1)
        modified_plus_month = self.modified.date() + relativedelta(months=1)

        # last login + two weeks
        last_login_plus_two_weeks = self.poster.last_login.date() +\
            relativedelta(weeks=2)

        last_poked = ((today > created_plus_month) or (today > modified_plus_month))
        recent_login = (today > last_login_plus_two_weeks)

        if last_poked and recent_login:
            return False
        else:
            return True

    def bids(self):
        return Bid.objects.filter(listing=self)

    def final_price(self):
        try:
            price = self.winning_bid.price
        except:
            price = None
        return price

    # retrieve url for object
    def get_absolute_url(self):
        return reverse('detail_listing', kwargs={'slug': self.slug})

    # object call
    def __unicode__(self):
        return '%s : %s' % (self.isbn, self.title)

    class Meta:
        # unique_together = (("ISBN", "poster"),)
        ordering = ['isbn', 'title']


class Bid(TimeStampedModel):

    bidder = models.ForeignKey(Student)
    listing = models.ForeignKey(Listing)
    price = models.PositiveIntegerField(default=0,
                                        validators=[MaxValueValidator(1000)],)
    text = models.CharField(blank=True, max_length=2000,)

    slug = RandomSlugField(length=6)

    def __unicode__(self):
        return '%s\'s bid for $%s' % (self.bidder, str(self.price))

    class Meta:
        ordering = ['-created']


class Flag(TimeStampedModel):

    WRONG_PRODUCT_TYPE = 'Not a Textbook'
    # may eventually change as additional product categories are added
    OBSCENE = 'Obscene'
    SPAM = 'Spam'
    COPYRIGHT = 'Copyright Violation'
    ILLEGAL = 'Otherwise Illegal'

    FLAGGING_REASON_CHOICES = (
        (WRONG_PRODUCT_TYPE, 'Not a Textbook'),
        (OBSCENE, 'Obscene'),
        (SPAM, 'Spam'),
        (COPYRIGHT, 'Copyright Violation'),
        (ILLEGAL, 'Otherwise Illegal'),
    )

    flagger = models.ForeignKey(Student)
    listing = models.ForeignKey(Listing)

    reason = models.CharField(choices=FLAGGING_REASON_CHOICES, max_length=30,)

    slug = RandomSlugField(length=6)

    def __unicode__(self):
        return "%s's %s for %s" % (self.flagger.user.username,
                                   self.listing.title,
                                   self.reason)

    class Meta:
        ordering = ['listing', 'created']


class Rating(TimeStampedModel):

    ONE_STAR = '1'
    TWO_STAR = '2'
    THREE_STAR = '3'
    FOUR_STAR = '4'
    FIVE_STAR = '5'

    STAR_CHOICES = (
        (ONE_STAR, '1'),
        (TWO_STAR, '2'),
        (THREE_STAR, '3'),
        (FOUR_STAR, '4'),
        (FIVE_STAR, '5'),
    )

    rater = models.ForeignKey(Student)
    listing = models.ForeignKey(Listing)

    stars = models.CharField(choices=STAR_CHOICES, max_length=10,)
    review = models.TextField(blank=True, max_length=3000,)

    slug = RandomSlugField(length=6)

    def __unicode__(self):
        return "%s's review of %s" % (self.rater.user.username,
                                      self.listing.poster.user.username)

    class Meta:
        ordering = ['rater', 'listing', 'created']
