from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
# Create your models here.



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
