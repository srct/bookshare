from django.db import models
from django.forms import ModelForm, Textarea, TextInput, NumberInput, Select, FileInput
from website.models import Seller, Listing


BOOK_CONDITION_CHOICES = (
    ('0', 'New'),
    ('1', 'Like New'),
    ('2', 'Very Good'),
    ('3', 'Good'),
    ('4', 'Acceptable'),
    ('5', 'Unacceptable'),
)

class ListingForm( ModelForm ):
    class Meta:
        model = Listing
        fields = ('ISBN', 'title', 'author', 'year', 'edition',
        'book_condition', 'price', 'description', 'photo')
        exclude = ('seller', 'date_created', 'date_sold', 'sold',
        'finalPrice', 'slug')
        widgets = {
            'ISBN': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Book ISBN',
            }),
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Book Title',
            }),
            'author': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Book Author',
            }),
            'year': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Year Published',
            }),
            'edition': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Book Edition',
            }),
            'condition': Select(attrs={
                'class': 'form-control',
            }),
            'price': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Asking Price',
            }),
            'description': Textarea(attrs={
                'row': 3,
                'class': 'form-control',
            }),
            'photo': FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Asking Price',
            }),
        }
