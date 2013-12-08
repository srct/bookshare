from django.core.exceptions import ValidationError
from django.db import models
from django.forms import ModelForm, Textarea, TextInput, NumberInput, Select, FileInput
from website.models import Seller, Listing


class ListingForm( ModelForm ):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ListingForm, self).__init__(*args, **kwargs)

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
        cleaned_data = super(ListingForm, self).clean()

        try:
            print "IM TRYING BUT IDK WHATS HAPPENING TO ME"
            print cleaned_data
            cleaned_isbn = cleaned_data.get('ISBN')
            cleaned_seller = self.request.user.seller

            b = Listing.objects.get(ISBN=cleaned_isbn,
                                    seller=cleaned_seller)
            print "Succeeded."
            print b
        #except Listing.DoesNotExist:
        except Listing.DoesNotExist as e:
            print "AN ERROR OCCURRECDD"
            print e
            print type(e)
            pass
        else:
            raise ValidationError("Listing with this ISBN already exists for this seller.")
        return cleaned_data
