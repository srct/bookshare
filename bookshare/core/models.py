from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel
from django.core.validators import RegexValidator

# Create your models here.
class Course(TimeStampedModel):
	name = models.CharField(max_length=255)
	department = models.CharField(max_length=255)
	number = models.CharField(max_length=255, validators=RegexValidator('[0-9]{3,}'))

	def __unicode__(self):
		return "%s:%s  %s", self.department, self.number, self.name