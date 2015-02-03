from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder, HTML, Field
#from crispy_forms.bootstrap import PrependedText

from lookouts.models import Lookout

class LookoutForm( forms.ModelForm ):

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset("Your Layout",
                'isbn',
            ),
        )

        self.helper.add_input(Submit('submit', 'Submit'))

        super(LookoutForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Lookout

class DeleteLookoutForm( forms.Form ):
    lookout_id = forms.IntegerField(
        required = True,
        widget=forms.HiddenInput()
    )
