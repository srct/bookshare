from django.core.exceptions import ValidationError
from django import forms
from django.db import models
from django.forms import ModelForm, Textarea, TextInput, NumberInput, Select, FileInput
from website.models import Seller, Listing


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
        fields = ('ISBN', 'title', 'author', 'year', 'edition',
        'book_condition', 'price', 'description', 'photo')
        exclude = ('seller', 'date_created', 'date_sold', 'sold',
        'finalPrice')
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
                #'class': 'form-control',
                'placeholder': 'Asking Price',
            }),
        }

    def clean(self):
        error_message = "You've already posted a listing with this ISBN. Close that listing first."
        cleaned_data = super(ListingForm, self).clean()

        cleaned_isbn = cleaned_data.get('ISBN')
        cleaned_seller = self.request.user.seller

        existing_listings = Listing.objects.filter(ISBN=cleaned_isbn,
                                                    seller=cleaned_seller,
                                                    active=True)

        if len( existing_listings ) > 0:
            raise ValidationError(error_message)

        return cleaned_data
