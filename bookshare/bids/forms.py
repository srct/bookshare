from django.db import models
from django import forms
from bids.models import Bid


class BidForm( forms.ModelForm ):
    class Meta:
        model = Bid
        fields = ('price', 'text')
        exclude = ('bidder', 'listing', 'date_created')
        labels = {
            'price': 'Offer',
            'text': 'Comments (Optional)',
        }
        widgets = {
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
        }
