from django.db import models
from django.forms import ModelForm,Textarea

from website.models import Seller, Listing


BOOK_CONDITION_CHOICES = (
    ('0', 'Like New'),
    ('1', 'Very Good'),
    ('2', 'Good'),
    ('3', 'Acceptable'),
)

class ListingForm( ModelForm ):
    class Meta:
        model = Listing
        fields = ['title', 'author', 'ISBN', 'year', 'edition',
        'book_condition', 'description', 'price', 'photo']
        widgets = {
            'description' : Textarea(attrs={'cols':80,'row':20}),
        }
