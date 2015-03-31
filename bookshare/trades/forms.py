from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, Field
from crispy_forms.bootstrap import AppendedPrependedText, FormActions

from trades.models import Listing, Bid

class ListingForm( forms.ModelForm ):

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-sm-2'
        self.helper.field_class='col-sm-6'

        self.helper.layout = Layout(
            Fieldset("",
                'seller',
                'isbn',
                HTML("""<hr/ >"""),
                Field('title'),
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
                 FormActions(Submit('submit', 'Submit', css_class='btn-primary'))
            ),
        )

        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields['isbn'].label = "ISBN"

    class Meta:
        model = Listing
        exclude = ('data_sold', 'sold', 'active', 'finalPrice')

class BidForm( forms.ModelForm ):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class='form-horizontal'

        self.helper.layout = Layout(
            Fieldset("",
                'bidder',
                'listing',
                HTML("<div class='col-md-4'>"),
                 AppendedPrependedText('price','$', '.00', placeholder="whole numbers"),
                HTML("</div><div class='col-md-4'>"),
                'text',
                HTML("</div><div class='col-md-4'>"),
                 FormActions(Submit('submit', 'Submit', css_class='btn-primary')),
                HTML("</div>"),
            ),
        )
        super(BidForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = "Comments"

    class Meta:
        model = Bid

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


