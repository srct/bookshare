from django.db import models

# Create your models here.
class Book( models.Mode ):
    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 200)
    ISBN = models.CharField(max_length = 200)

    uploaded = models.DateField(auto_add_now)
    
    condition = TextField()

    sold = models.BooleanField()

    price = models.IntegerField()

    # for later with moar space --> image upload

    # slugfield
