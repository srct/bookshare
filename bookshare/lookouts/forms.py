from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Submit, Layout, Fieldset, HTML, Field
from crispy_forms.bootstrap import FormActions

from .models import Lookout


class LookoutForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.label_class = 'col-md-2 col-md-offset-1 text-center be-bold'
        self.helper.field_class = 'col-sm-8'

        self.helper.layout = Layout(
            Fieldset("",
                     Field('isbn', placeholder='0801884039'),
                     HTML("""<hr/ >"""),
                     FormActions(Submit('submit', 'Submit',
                                        css_class='btn-primary'),
                                 Button('cancel', 'Never Mind',
                                        css_class="btn-default",
                                        onclick="history.back()")
                                 ),
                     ),
        )

        super(LookoutForm, self).__init__(*args, **kwargs)
        self.fields['isbn'].label = "ISBN"

    class Meta:
        model = Lookout
