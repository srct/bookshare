# core django imports
from django import forms
# third-pary imports
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit, Layout, Fieldset, HTML, Field
from crispy_forms.bootstrap import FormActions

from .models import Lookout


class LookoutForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LookoutForm, self).__init__(*args, **kwargs)

        # Define the basics for crispy-forms
        self.helper = FormHelper()
        # Some extra vars for form css purposes
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2 be-bold bottom-padding'
        self.helper.field_class = 'col-lg-8 bottom-padding'

        # Label the 'isbn' field
        self.fields['isbn'].label = "ISBN"

        self.helper.layout = Layout(
            Fieldset("",
                Field('isbn', placeholder='0801884039', style="width: 155px;"),

                FormActions(
                    Submit('submit', 'Submit', css_class='btn-primary'),
                    Button('cancel', 'Never Mind', css_class="btn-default",
                        onclick="history.back()")
                ),
            ),
        )

    class Meta:
        model = Lookout
        fields = ['isbn',]
