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

    pf_first_name = models.CharField(max_length=255, blank=True)
    pf_last_name = models.CharField(max_length=255, blank=True)

    slug = AutoSlugField(populate_from='user', unique=True)

    emails_sent = models.PositiveIntegerField(default=0)

    def get_full_name(self):
        if not(self.user.get_full_name()):
            return self.user.username
        else:
            return self.user.get_full_name()

    def has_nickname(self):
        pf_name = "%s %s" % (self.pf_first_name, self.pf_last_name)

        if (self.user.get_full_name() != pf_name) and (pf_name != " "):
            return True
        else:
            return False

    def get_nickname(self):
        # different first name
        if (self.user.first_name != self.pf_first_name) and (self.user.last_name == self.pf_last_name):
            return "%s \"%s\" %s" % (self.pf_first_name, self.user.first_name, self.user.last_name)
        # different last name
        elif (self.user.first_name == self.pf_first_name) and (self.user.last_name != self.pf_last_name):
            return "%s %s \"%s\"" % (self.user.first_name, self.pf_last_name, self.user.last_name)
        # both
        elif (self.user.first_name != self.pf_first_name) and (self.user.last_name != self.pf_last_name):
            return "%s \"%s %s\" %s" % (self.pf_first_name, self.user.first_name, self.user.last_name, self.pf_last_name)
        # failing gracefully
        else:
            return self.user.get_full_name()

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
