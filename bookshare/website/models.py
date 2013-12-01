from django.db import models

# Create your models here.
class Listing( models.Model ):
    seller = models.ForeignKey('Seller')

    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 200)
    ISBN = models.CharField(max_length = 15)

    date_created = models.DateField()
    date_sold = models.DateField()
    condition = models.TextField()
    description = models.TextField()
    price = models.IntegerField()
    photo = models.ImageField(max_length = 1000,upload_to='listing_photos')

    sold = models.BooleanField()

    slug = models.SlugField(max_length = 50)

    # object call
    def __unicode__(self):
        return '%s' % self.title


class Seller( models.Model ):

    name = models.CharField(max_length = 200, primary_key=True)
    email = models.CharField(max_length = 200)

    listings = models.ManyToManyField('Listing', blank=True, related_name='+')

    # object call
    def __unicode__(self):
        return '%s' % self.name
