from django.db import models
from django import forms
from bids.models import Bid


class BidForm( forms.ModelForm ):

    def clean(self):
        cleaned_data = super(BidForm, self).clean()
        bidder = cleaned_data.get('bidder')
        listing = cleaned_data.get('listing')
        if bidder == listing.seller:
            raise forms.ValidationError(u"You can't bid on your own listing!")
        return cleaned_data

    class Meta:
        model = Bid
        fields = ('price', 'text', 'bidder', 'listing',)
        exclude = ('date_created',)
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
