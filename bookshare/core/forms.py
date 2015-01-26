from haystack.forms import SearchForm

class StyledSearchForm( SearchForm ):
    q = forms.CharField(
        required = False,
        label = 'Search',
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ISBN, Title, Author',
            'autofocus': 'autofocus',
        }),
    )


