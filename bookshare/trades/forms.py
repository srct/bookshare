# core django imports
from django import forms
# third party imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit, Layout, Fieldset, HTML, Field
from crispy_forms.bootstrap import AppendedPrependedText, FormActions
# imports from your apps
from .models import Listing, Bid, Flag, Rating


class ListingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        # bootstrap3 formatting
        self.helper.label_class = 'col-md-3 be-bold'
        self.helper.field_class = 'col-md-9 bottom-padding'

        self.helper.layout = Layout(
            Fieldset("",
                     Field('isbn', placeholder='0801884039'),
                     HTML('<div class="collapse" id="section-collapse">'),
                     Field('title',
                           placeholder='Squirrels: The Animal Answer Guide'),
                     Field('author',
                           placeholder='Richard W. Thorington, Jr., and Katie Ferrell'),
                     Field('edition', placeholder='1'),
                     Field('year', placeholder='2006'),
                     HTML('</div>'),
                     Field('course_abbr', placeholder='ENGH 302'),
                     'condition',
                     'access_code',
                     AppendedPrependedText('price', '$', '.00',
                                           placeholder="whole numbers"),
                     'photo',
                     Field('description',
                           placeholder='I would be willing to exchange this textbook for one that I need next semester. /// This is for Professor Smith\'s section ONLY. /// I can give you the workbook as well.'),
                     FormActions(Submit('submit', 'Create',
                                 css_class='btn-primary'),
                                 Button('cancel', 'Never Mind',
                                        css_class='btn-default',
                                        onclick="history.back()")
                                 ),

                     ),
        )

        super(ListingForm, self).__init__(*args, **kwargs)
        self.fields['isbn'].label = "ISBN"
        self.fields['course_abbr'].label = "Course"
        self.fields['description'].label = "Other Notes"
        self.fields['photo'].required = False

    class Meta:
        model = Listing


class BidForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.label_class = 'be-bold col-md-2'
        self.helper.field_class = 'col-md-10'

        self.helper.layout = Layout(
            Fieldset("",
                     'listing',
                     HTML("<div class='col-md-4'>"),
                     AppendedPrependedText('price', '$', '.00',
                                           placeholder="whole numbers"),
                     HTML("</div><div class='col-md-6'>"),
                     'text',
                     HTML("</div><div class='col-md-2'>"),
                     FormActions(Submit('submit', 'Submit',
                                        css_class='btn-primary')
                                 ),
                     HTML("</div>"),
                     ),
        )

        super(BidForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = "Comments"

    class Meta:
        model = Bid


class FlagForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()

        self.helper.label_class = 'be-bold'
        self.helper.layout = Layout(
            Fieldset("",
                     'reason',
                     HTML("""<hr/ >"""),
                     FormActions(Submit('submit', 'Create',
                                        css_class='btn-primary'),
                                 Button('cancel', 'Never Mind',
                                        css_class='btn-default',
                                        onclick="history.back()")
                                 ),
                     ),
        )
        super(FlagForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Flag

#class EditListingForm( forms.ModelForm ):


class ExchangeListingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()

        self.helper.label_class = 'be-bold'
        self.helper.layout = Layout(
            Fieldset("",
                     'winning_bid',
                     HTML("""<hr/ >"""),
                     HTML("""<strong>Your Email to Your Bidder</strong>"""),
                     HTML("""<div class="well"><em><p>Hey there!</p><p>Poster {{ listing.poster.user.get_full_name }} has picked your bid for {{ listing.title }} on SRCT Bookshare. They're the cc'ed email address-- {{ listing.poster.user.email }}.</p><p>Watch your email to arrange all the final touches to get your book.</p></em>"""),
                     Field('email_message',
                           placeholder='Do you want to meet tomorrow by the JC Info Desk at 4?'),
                     HTML("""<em><p>Thanks for using SRCT Bookshare!</p><p>Mason SRCT</p></em></div>"""),
                     HTML("""<hr/ >"""),
                     HTML("""<div class="text-center">Friendly reminder: Don't spam people. We will deactivate your account.</div>"""),
                     HTML("""<hr/ >"""),
                     FormActions(Submit('submit', 'Email and Exchange',
                                        css_class='btn-primary'),
                                 Button('cancel', 'Never Mind',
                                        css_class='btn-default',
                                        onclick="history.back()")
                                 ),
                     ),
        )

        super(ExchangeListingForm, self).__init__(*args, **kwargs)
        self.fields['email_message'].label = "Custom Message"
        self.fields['winning_bid'].required = True
        self.fields['email_message'].initial = ''

    class Meta:
        model = Listing


class UnExchangeListingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()

        self.helper.label_class = 'be-bold'
        self.helper.layout = Layout(
            Fieldset("",
                     HTML("""<strong>Your Email to Your Bidder</strong>"""),
                     HTML("""<div class="well"><em><p>Hey there!</p><p>Poster {{ listing.poster.user.get_full_name }} has cancelled your bid for {{ listing.title }} on SRCT Bookshare.</p><p>We certainly hope that this doesn't come as a shock. :-P</p><p>(If you don't know why you're getting this email, hey're the cc'ed email address-- {{ listing.poster.user.email }}. Contact them ASAP to clear up any confusion.)<p></em>"""),
                     Field('email_message',                           placeholder='I haven\'t heard from you in a couple of days, so I\'m going to have to try to exchange my textbook to someone else. :-/'),
                     HTML("""<em><p>Thanks for using SRCT Bookshare!</p><p>Mason SRCT</p></em></div>"""),
                     HTML("""<hr/ >"""),
                     HTML("""<div class="text-center">Friendly reminder: Don't spam people. We will deactivate your account.</div>"""),
                     HTML("""<hr/ >"""),
                     FormActions(Submit('submit', 'Email and Cancel Exchange',
                                        css_class='btn-primary'),
                                 Button('cancel', 'Never Mind',
                                        css_class='btn-default',
                                        onclick="history.back()")
                                 ),
                     ),
        )

        super(UnExchangeListingForm, self).__init__(*args, **kwargs)
        self.fields['email_message'].label = "Custom Message"
        self.fields['email_message'].initial = ''

    class Meta:
        model = Listing


class RatingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()

        self.helper.label_class = 'be-bold'
        self.helper.layout = Layout(
            Fieldset("",
                     'stars',
                     'review',
                     HTML("""<hr/ >"""),
                     FormActions(Submit('submit', 'Create',
                                        css_class='btn-primary'),
                                 Button('cancel', 'Never Mind',
                                        css_class='btn-default',
                                        onclick="history.back()")
                                 ),
                     ),
        )
        super(RatingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Rating
