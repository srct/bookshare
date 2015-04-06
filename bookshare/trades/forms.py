from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, Field
from crispy_forms.bootstrap import AppendedPrependedText, FormActions

from trades.models import Listing, Bid, Flag

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
                Field('isbn', placeholder='0801884039'),
                HTML("""<hr/ >"""),
                Field('title', placeholder='Squirrels: The Animal Answer Guide'),
                Field('author', placeholder='Richard W. Thorington, Jr., and Katie Ferrell'),
                'edition',
                Field('year', placeholder='2006'),
                HTML("""<hr/ >"""),
                #'course',
                'condition',
                'access_code',
                AppendedPrependedText('price','$', '.00', placeholder="whole numbers"),
                'photo',
                Field('description', placeholder='I would be willing to exchange this textbook for one that I need next semester.'),
                HTML("""<hr/ >"""),
                FormActions(Submit('submit', 'Create', css_class='btn-primary'))
            ),
        )

        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields['isbn'].label = "ISBN"

    class Meta:
        model = Listing
        exclude = ('sold', 'cancelled', 'email_message', 'winning_bid', 'date_closed')

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

class FlagForm( forms.ModelForm ):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class='form-horizontal'

        self.helper.layout = Layout(
            Fieldset("",
            'flagger',
            'listing',
            'reason',
             HTML("""<hr/ >"""),
             FormActions(Submit('submit', 'Create', css_class='btn-primary'))
            ),
        )
        super(FlagForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Flag

#class EditListingForm( forms.ModelForm ):

class SellListingForm( forms.ModelForm ):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class='form-horizontal'

        self.helper.layout = Layout(
            Fieldset("",
                'sold',
                'winning_bid',
                'date_closed',
                HTML("""<hr/ >"""),
                HTML("""<strong>Your Email to Your Bidder</strong>"""),
                HTML("""<div class="well"><em><p>Hey there!</p><p>Seller {{ listing.seller.user.first_name }} {{ listing.seller.user.last_name }} has picked your bid for {{ listing.title }} on SRCT Bookshare. They're the cc'ed email address-- {{ listing.seller.user.email }}.</p><p>Watch your email to arrange all the final touches to get your book.</p></em>"""),
                'email_message',
                HTML("""<em><p>Thanks for using SRCT Bookshare!</p><p>Mason SRCT</p></em></div>"""),
                HTML("""<hr/ >"""),
                # cancel button
                FormActions(Submit('submit', 'Email and Sell', css_class='btn-primary'))
            ),
        )
        super(SellListingForm, self).__init__(*args, **kwargs)
        self.fields['email_message'].label = "Custom message (optional)"

    class Meta:
        model = Listing
        exclude = ('seller', 'title', 'author', 'isbn', 'year', 'edition', 'condition', 'access_code', 'description', 'price', 'photo', 'cancelled', )

class UnSellListingForm( forms.ModelForm ):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class='form-horizontal'

        self.helper.layout = Layout(
            Fieldset("",
                'sold',
                'winning_bid',
                'date_closed',
                # cancel button
                FormActions(Submit('submit', 'Back on the Market', css_class='btn-primary'))
            ),
        )
        super(UnSellListingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Listing
        exclude = ('seller', 'title', 'author', 'isbn', 'year', 'edition', 'condition', 'accss_code', 'description', 'price', 'photo', 'cancelled', 'email_message')

class CancelListingForm( forms.ModelForm ):

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class='form-horizontal'

        self.helper.layout = Layout(
            Fieldset("",
                'cancelled',
                'date_closed',
                # cancel button
                 FormActions(Submit('submit', 'Cancel Your Listing', css_class='btn-primary'))
            ),
        )
        super(CancelListingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Listing
        exclude = ('seller', 'title', 'author', 'isbn', 'year', 'edition', 'condition', 'access_code', 'description', 'price', 'photo', 'sold', 'email_message', 'winning_bid',)

class ReopenListingForm( forms.ModelForm ):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class='form-horizontal'

        self.helper.layout = Layout(
            Fieldset("",
                'cancelled',
                # cancel button
                 FormActions(Submit('submit', 'Reopen Your Listing', css_class='btn-primary'))
            ),
        )
        super(ReopenListingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Listing
        exclude = ('seller', 'title', 'author', 'isbn', 'year', 'edition', 'condition', 'access_code', 'description', 'price', 'photo', 'sold', 'email_message', 'winning_bid', 'date_closed')
