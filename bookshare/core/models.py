from django.db import models
#from django.conf import settings
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
from django.core.validators import RegexValidator

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

#post_save.connect(create_user_profile, sender=User)

class Course(TimeStampedModel):
	name = models.CharField(max_length=255)
	department = models.CharField(max_length=255)
        departmentAbbreviation = models.CharField(max_length=4)
	#number = models.CharField(max_length=255, validators=RegexValidator('[0-9]{3,}'))
	number = models.CharField(max_length=3)

	def __unicode__(self):
		return "%s:%s  %s", self.department, self.number, self.name
