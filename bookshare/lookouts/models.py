# core django imports
from django.db import models
from django.urls import reverse
from django.core.validators import RegexValidator
# third-party imports
from model_utils.models import TimeStampedModel
from randomslugfield import RandomSlugField
# imports from your apps
from trades.models import Listing
from trades.utils import ISBNMetadata
from core.models import Student


class Lookout(TimeStampedModel):
    owner = models.ForeignKey(Student,
                              on_delete=models.CASCADE)
    isbn = models.CharField(
        max_length=20,
        validators=[RegexValidator('[0-9xX-]{10,20}',
                    message='Please enter a valid ISBN.')])


    title = models.CharField(max_length=200,
                             null=True, blank=True)

    author = models.CharField(max_length=200,
                              null=True, blank=True)

    # would have to load in every conceivable course first
    # course = models.ForeignKey(Course)
    slug = RandomSlugField(length=6)

    def get_listings(self):
        isbn_listings = models.Q(isbn=self.isbn, exchanged=False, cancelled=False)
        return Listing.objects.filter(isbn_listings)

    def get_title_or_isbn(self):
        if self.title:
            return self.title
        else:
            return self.isbn

    def get_absolute_url(self):
        return reverse('detail_lookout', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not(self.title):  # only run when initially created
            isbn_metadata = ISBNMetadata(self.isbn)
            self.title = isbn_metadata.get('title')
            self.author = isbn_metadata.get('authors')
        super().save(*args, **kwargs)

    def __unicode__(self):
        return '%s %s' % (self.owner.user.username, self.isbn)

    class Meta:
        ordering = ['isbn']
        # a student can't create the same lookout twice
        unique_together = ['owner', 'isbn']
