from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit, Layout, Fieldset, HTML, Field
from crispy_forms.bootstrap import AppendedPrependedText, FormActions

from trades.models import Listing, Bid, Flag

class ListingForm( forms.ModelForm ):

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()

        # bootstrap3 formatting
        self.helper.label_class='col-md-3 be-bold'
        self.helper.field_class='col-md-9 bottom-padding'

        self.helper.layout = Layout(
            Fieldset("",
                'seller',
                Field('isbn', placeholder='0801884039'),
                Field('title', placeholder='Squirrels: The Animal Answer Guide'),
                Field('author', placeholder='Richard W. Thorington, Jr., and Katie Ferrell'),
                'edition',
                Field('year', placeholder='2006'),
                #'course',
                'condition',
                'access_code',
                AppendedPrependedText('price','$', '.00', placeholder="whole numbers"),
                'photo',
                Field('description', placeholder='I would be willing to exchange this textbook for one that I need next semester. /// This is for Professor Smith\'s section ONLY. /// I can give you the workbook as well.'),
                FormActions(
                Submit('submit', 'Create', css_class='btn-primary'),
                Button('cancel', 'Never Mind', css_class='btn-default', onclick="history.back()")),

            ),
        )

        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields['isbn'].label = "ISBN"
        self.fields['description'].label = "Other Notes"

    class Meta:
        model = Listing
        include = ('seller', 'isbn', 'title', 'author', 'edition', 'year', 'condition', 'access_code', 'price', 'photo', 'description',)

class BidForm( forms.ModelForm ):

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()

        # bootstrap3 formatting
        self.helper.label_class='be-bold col-md-2'
        self.helper.field_class='col-md-10'

        self.helper.layout = Layout(
            Fieldset("",
                'bidder',
                'listing',
                HTML("<div class='col-md-4'>"),
                 AppendedPrependedText('price','$', '.00', placeholder="whole numbers"),
                HTML("</div><div class='col-md-6'>"),
                'text',
                HTML("</div><div class='col-md-2'>"),
                FormActions(Submit('submit', 'Submit', css_class='btn-primary')),
                HTML("</div>"),
            ),
        )
        super(BidForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = "Comments"

    class Meta:
        model = Bid
        include = ('bidder', 'listing', 'price', 'text',)

class FlagForm( forms.ModelForm ):

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()

        # bootstrap3 formatting
        self.helper.label_class='be-bold'

        self.helper.layout = Layout(
            Fieldset("",
            'flagger',
            'listing',
            'reason',
             HTML("""<hr/ >"""),
             FormActions(
                 Submit('submit', 'Create', css_class='btn-primary'),
                 Button('cancel', 'Never Mind', css_class='btn-default', onclick="history.back()")),
            ),
        )
        super(FlagForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Flag
        include = ('flagger', 'listing', 'reason',)

#class EditListingForm( forms.ModelForm ):

class SellListingForm( forms.ModelForm ):

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.label_class='be-bold'

        self.helper.layout = Layout(
            Fieldset("",
                'sold',
                'winning_bid',
                'date_closed',
                HTML("""<hr/ >"""),
                HTML("""<strong>Your Email to Your Bidder</strong>"""),
                HTML("""<div class="well"><em><p>Hey there!</p><p>Seller {{ listing.seller.user.first_name }} {{ listing.seller.user.last_name }} has picked your bid for {{ listing.title }} on SRCT Bookshare. They're the cc'ed email address-- {{ listing.seller.user.email }}.</p><p>Watch your email to arrange all the final touches to get your book.</p></em>"""),
                Field('email_message', placeholder='Do you want to meet tomorrow by the JC Info Desk at 4?'),
                HTML("""<em><p>Thanks for using SRCT Bookshare!</p><p>Mason SRCT</p></em></div>"""),
                HTML("""<hr/ >"""),
                FormActions(
                Submit('submit', 'Email and Sell', css_class='btn-primary'),
                Button('cancel', 'Never Mind', css_class='btn-default', onclick="history.back()")),
            ),
        )
        super(SellListingForm, self).__init__(*args, **kwargs)
        self.fields['email_message'].label = "Custom Message"

    class Meta:
        model = Listing
        include = ('sold', 'winning_bid', 'date_closed', 'email_message',)

class UnSellListingForm( forms.ModelForm ):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Fieldset("",
                'sold',
                'winning_bid',
                'date_closed',
                 FormActions(
                 Submit('submit', 'Back on the Market', css_class='btn-primary'),
                 Button('cancel', 'Never Mind', css_class='btn-default', onclick="history.back()")),
            ),
        )
        super(UnSellListingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Listing
        include = ('sold', 'winning_bid', 'date_closed',)

class CancelListingForm( forms.ModelForm ):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Fieldset("",
                'cancelled',
                'date_closed',
                 FormActions(
                 Submit('submit', 'Cancel Your Listing', css_class='btn-primary'),
                 Button('cancel', 'Never Mind', css_class='btn-default', onclick="history.back()")),
            ),
        )
        super(CancelListingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Listing
        include = ('cancelled', 'date_closed',)

class ReopenListingForm( forms.ModelForm ):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()

        self.helper.layout = Layout(
            Fieldset("",
                'cancelled',
                'date_closed',
                 FormActions(
                 Submit('submit', 'Reopen Your Listing', css_class='btn-primary'),
                 Button('cancel', 'Never Mind', css_class='btn-default', onclick="history.back()")),
            ),
        )
        super(ReopenListingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Listing
        include = ('cancelled', 'date_closed',)
