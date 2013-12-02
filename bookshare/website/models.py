from django.db import models

# Create your models here.
class Listing( models.Model ):
    seller = models.ForeignKey('Seller')

    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 200)
    ISBN = models.CharField(max_length = 15)
    year = models.IntegerField()
    edition = models.CharField(max_length = 30)

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

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('listing', args=[self.seller.username, str(self.id)])


class Seller( models.Model ):

    name = models.CharField(max_length = 200, primary_key=True)
    username = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200)

    # object call
    def __unicode__(self):
        return '%s' % self.name
