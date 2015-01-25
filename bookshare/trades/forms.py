from django.db import models
from django import forms
from trades.models import Bid

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

from django.core.exceptions import ValidationError
from django.forms import ModelForm, Textarea, TextInput, NumberInput, Select, FileInput
from trades.models import Listing#, Seller # where did we put seller?
from haystack.forms import SearchForm


class StyledSearchForm( SearchForm ):
    q = forms.CharField(
        required = False,
        label = 'Search',
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ISBN, Title, Author',
            'autofocus': 'autofocus',
        }),
    )


class FinalPriceForm( forms.Form ):
    book_id = forms.IntegerField(
        required = True,
        widget=forms.HiddenInput(),
    )
    final_price = forms.CharField(
        required = False,
        label = 'Final Selling Price',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        }),
    )


class CloseForm( forms.Form ):
    book_id = forms.IntegerField(
        required = True,
        widget=forms.HiddenInput(),
    )


class ListingForm( ModelForm ):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ListingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Listing
        fields = ('isbn', 'title', 'author', 'year', 'edition',
        'book_condition', 'price', 'description', 'photo')
        exclude = ('seller', 'date_created', 'date_sold', 'sold',
        'finalPrice')
        labels = {
            'isbn': 'ISBN',
            'title': 'Title',
            'author': 'Author',
            'year': 'Year',
            'edition': 'Edition',
            'book_condition': 'Condition',
            'price': 'Price',
            'description': 'Description',
            'photo': 'Photo',
        }
        widgets = {
            'isbn': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Book ISBN',
                'pattern': '[0-9xX-]{10,20}',
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
            'book_condition': Select(attrs={
                'class': 'form-control',
            }),
            'price': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Asking Price',
            }),
            'description': Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
            }),
            'photo': FileInput(attrs={
                'placeholder': 'Asking Price',
            }),
        }

    def clean(self):
        error_message = "You've already posted a listing with this ISBN. Close that listing first."
        cleaned_data = super(ListingForm, self).clean()

        cleaned_isbn = cleaned_data.get('isbn')
        cleaned_seller = self.request.user.seller

        existing_listings = Listing.objects.filter(isbn=cleaned_isbn,
                                                    seller=cleaned_seller,
                                                    active=True)

        if len( existing_listings ) > 0:
            raise ValidationError(error_message)

        return cleaned_data
