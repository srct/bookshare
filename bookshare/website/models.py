from django.db import models

# Create your models here.
class Listing( models.Mode ):

    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 200)
    ISBN = models.CharField(min_length = 10, max_length = 15)

    date_created = models.DateField(auto_add_now)
    condition = TextField()
    price = models.IntegerField()
    photo = models.ImageField(max_length = 1000)

    sold = models.BooleanField()

    slug = models.SlugField(max_length = 50)

    # object call
    def __unicode__(self):
        return '%s' % self.title


class Seller( models.Mode ):

    name = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200)

    listings = models.ManyToManyField('Listing', blank=True)
