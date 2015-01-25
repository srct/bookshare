from django import forms
from django.forms import ModelForm, TextInput
from lookouts.models import Lookout

class LookoutForm( ModelForm ):
    class Meta:
        model = Lookout
        fields = ['isbn']
        exclude = ['owner', 'date_created']
        labels = {
            'isbn': 'ISBN',
        }
        widgets = {
            'isbn': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Book ISBN',
                'pattern': '[0-9xX-]{10,20}',
            }),
        }

class DeleteLookoutForm( forms.Form ):
    lookout_id = forms.IntegerField(
        required = True,
        widget=forms.HiddenInput()
    )
