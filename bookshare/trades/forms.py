from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, HTML, Field
from crispy_forms.bootstrap import AppendedPrependedText

from trades.models import Listing, Bid

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

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class='form-horizontal'
        self.helper.layout = Layout(
             Fieldset("Your Textbook",
                 Field('isbn', title="ISBN"),
                 HTML("""<hr/ >"""),
                 'title',
                 'author',
                 'edition',
                 'year',
                 HTML("""<hr/ >"""),
                 #'course',
                 'condition',
                 AppendedPrependedText('price','$', '.00', placeholder="whole numbers"),
                 'photo',
                 Field('description', placeholder='I would be willing to exchange this textbook for one that I need next semester'),
                 HTML("""<hr/ >"""),
             ),
        )

        self.helper.add_input(Submit('submit', 'Submit'))

        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields['isbn'].label = "ISBN"
        self.fields['description'].label = "Description/Comments"

    class Meta:
        model = Listing

#    def clean(self):
#        error_message = "You've already posted a listing with this ISBN. Close that listing first."
#        cleaned_data = super(ListingForm, self).clean()

#        cleaned_isbn = cleaned_data.get('isbn')
#        cleaned_seller = self.request.user.seller

#        existing_listings = Listing.objects.filter(isbn=cleaned_isbn,
#                                                    seller=cleaned_seller,
#                                                    active=True)

#        if len( existing_listings ) > 0:
#            raise ValidationError(error_message)

#        return cleaned_data
