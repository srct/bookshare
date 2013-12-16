from django.db import models
from django.forms import ModelForm, Textarea, NumberInput
from bids.models import Bid


class BidForm( ModelForm ):
    class Meta:
        model = Bid
        fields = ('price', 'text')
        exclude = ('bidder', 'listing', 'date_created')
        labels = {
            'price': 'Offer',
            'text': 'Comments (Optional)',
        }
        widgets = {
            'price': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price',
            }),
            'text': Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
        }
