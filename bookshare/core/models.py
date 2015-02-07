from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel
from django.core.validators import RegexValidator

class Student(TimeStampedModel):
    user = models.OneToOneField(User)
    # django user includes username, password, first name, and last name
    rating = models.IntegerField(null=True,default=0)

    slug = AutoSlugField(populate_from='user', unique=True)
    # populate from user.username, no?

    # needs a get_absolute_url ?

    def __unicode__(self):
        return '%s' % self.user.username

class Course(TimeStampedModel):
	name = models.CharField(max_length=255)
	department = models.CharField(max_length=255)
        departmentAbbreviation = models.CharField(max_length=4)
	#number = models.CharField(max_length=255, validators=RegexValidator('[0-9]{3,}'))
	number = models.CharField(max_length=3)

	def __unicode__(self):
		return "%s:%s  %s", self.department, self.number, self.name
