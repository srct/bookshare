from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, Field
from crispy_forms.bootstrap import FormActions

from lookouts.models import Lookout

class LookoutForm( forms.ModelForm ):

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class='col-sm-2'
        self.helper.field_class='col-sm-6'
    
        self.helper.layout = Layout(
            Fieldset("",
                'owner',
                'isbn',
                HTML("""<hr/ >"""),
                FormActions(Submit('submit', 'Submit', css_class='btn-primary'))
            ),
        )

        super(LookoutForm, self).__init__(*args, **kwargs)
        self.fields['isbn'].label = "ISBN"

    class Meta:
        model = Lookout
