# core django imports
from django.db import models
from django.contrib.auth.models import User
#from django.core.validators import RegexValidator
from django.core.urlresolvers import reverse
# third-party imports
from autoslug import AutoSlugField
from model_utils.models import TimeStampedModel


class Student(TimeStampedModel):
    # django user includes username, password, first name, and last name
    user = models.OneToOneField(User)

    slug = AutoSlugField(populate_from='user', unique=True)

    emails_sent = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})

    def __unicode__(self):
        return '%s' % self.user.username


class Course(TimeStampedModel):
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    departmentAbbreviation = models.CharField(max_length=4)
    # number = models.CharField(max_length=255,
                              # validators=RegexValidator('[0-9]{3,}'))
    number = models.CharField(max_length=3)

    def __unicode__(self):
        return "%s %s" % (self.departmentAbbreviation, self.number)
