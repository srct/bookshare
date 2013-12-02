from django.db import models

# Create your models here.
class Listing( models.Model ):
    seller = models.ForeignKey('Seller')

    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 200)
    ISBN = models.CharField(max_length = 15)
    year = models.IntegerField(null=True,blank=True)
    edition = models.CharField(blank=True,max_length = 30)

    date_created = models.DateTimeField()
    date_sold = models.DateField(null=True,blank=True)
    condition = models.TextField()
    description = models.TextField(blank=True)
    price = models.IntegerField()
    photo = models.ImageField(max_length = 1000,upload_to='listing_photos')

    sold = models.BooleanField()

    slug = models.SlugField(max_length = 50)

    finalPrice = models.IntegerField(null=True,blank=True)

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
    rating = models.IntegerField(null=True,blank=True)

    # object call
    def __unicode__(self):
        return '%s' % self.name
