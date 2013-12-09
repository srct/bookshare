from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.
class Listing( models.Model ):

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

    seller = models.ForeignKey('Seller')

    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 200)
    ISBN = models.CharField(max_length = 15)
    year = models.IntegerField(null=True,blank=True)
    edition = models.CharField(blank=True,max_length = 30)

    date_created = models.DateTimeField(default=timezone.now())
    date_sold = models.DateTimeField(null=True,blank=True)
    book_condition = models.CharField(choices=BOOK_CONDITION_CHOICES,
                                      max_length=20,
                                      default=GOOD)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    photo = models.ImageField(max_length = 1000,upload_to='listing_photos')

    sold = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    finalPrice = models.IntegerField(null=True,blank=True,default=0)

    # object call
    def __unicode__(self):
        if not self.active:
            return '[Inactive] %s : %s' % (self.ISBN, self.title)
        return '%s : %s' % (self.ISBN, self.title)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        if not self.active:
            return reverse('profile', args=[self.seller.user.username])
        return reverse('listing', args=[self.seller.user.username, str(self.id)])

    class Meta:
        #unique_together = (("ISBN", "seller"),)
        ordering = ['sold', '-ISBN']


class Seller( models.Model ):

    user = models.OneToOneField(User)
    #    name = models.CharField(max_length = 200, primary_key=True)
    #    username = models.CharField(max_length = 200)
    #    email = models.CharField(max_length = 200)
    rating = models.IntegerField(null=True,default=0)

    # object call
    def __unicode__(self):
        return '%s' % self.user

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('profile', args=[self.user.username])

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Seller.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
