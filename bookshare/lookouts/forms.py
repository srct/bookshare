from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, HTML, Field
from crispy_forms.bootstrap import FormActions

from lookouts.models import Lookout

class LookoutForm( forms.ModelForm ):

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.form_class = 'form-horizontal'
    helper.label_class='col-sm-2'
    helper.field_class='col-sm-6'
    
    helper.layout = Layout(
        Fieldset("Your Lookout",
            'owner',
            Field('isbn', title="ISBN"),
            HTML("""<hr/ >"""),
            FormActions(Submit('submit', 'Submit', css_class='btn-primary'))
        ),
    )

    class Meta:
        model = Lookout
