from django import template
from website.views import ISBNMetadata
register = template.Library()


@register.filter
def get_isbn_data( isbn, field ):
    data = ISBNMetadata( isbn )
    if data:
        return data.get(field)
    else:
        return "No data found."
