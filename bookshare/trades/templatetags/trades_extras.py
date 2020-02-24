from django import template
from trades.utils import ISBNMetadata

register = template.Library()


@register.filter(name='isbn_name')
def isbn_name(isbn):
    # numbers starting with 0 throw "SyntaxError: invalid token"
    isbn_str = str(isbn)
    data = ISBNMetadata(isbn_str)
    if data is not None:
        return data['title']
    else:
        return isbn_str


@register.filter(name='full_stars')
def full_stars(avg_stars):
    return range(int(avg_stars))


@register.filter(name='half_stars')
def half_stars(avg_stars):
    if (avg_stars % 1) >= .5:
        return True
    else:
        return False


@register.filter(name='empty_stars')
def empty_stars(avg_stars):
    if half_stars(avg_stars):
        return range(4 - int(avg_stars))
    else:
        return range(5 - int(avg_stars))


@register.filter(name='int_maker')
def int_maker(num):
    return int(num)

@register.filter(name='bc')
def bc(num):
    if num < 0:
        positive_value = str(abs(num))
        return "%s B.C." % (positive_value)
    else:
        return num
