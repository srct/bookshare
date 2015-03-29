from django import template
from trades.views import ISBNMetadata

register = template.Library()

@register.filter(name='isbn_name')
def isbn_name(isbn):
    # numbers starting with 0 throw "SyntaxError: invalid token"
    isbn_str = str(isbn)
    data = ISBNMetadata(isbn)
    if data is not None:
        return data['title']
    else:
        return isbn
