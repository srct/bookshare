# standard libary imports
from datetime import datetime
# third party imports
import requests
# imports from your apps
from .models import Flag, Rating, BidFlag


# previously pulled worldcat metadata from ISBNs, worldcat is now a paid service
# thankfully, the internet archive has stepped in with a free api replacement
def ISBNMetadata(standardISBN):
    # supports both ISBN 10 and ISBN 13
    key_format = 'ISBN:%s' % str(standardISBN)
    url = "https://openlibrary.org/api/books?bibkeys=" +\
          key_format +\
          "&format=json&jscmd=data"

    # In case the API fails to return, simply return None.
    try:
        metadata = requests.get(url, timeout=3)
    except requests.ConnectionError:
        return None

    # format into a dictionary
    json_response = metadata.json()
    isbn_data = json_response.get(key_format)
    try:
        title = isbn_data.get('title', '')
        subtitle = isbn_data.get('subtitle', '')
        if subtitle:
            full_title = '%s: %s' % (title, subtitle)
        else:
            full_title = title
        metadataDict = {'title': full_title}

        date = isbn_data.get('publish_date' ,'')
        # unfortunately, dates are formatted in a variety of different ways
        # but year should be the final four digits regardless of, say,  month formatting
        metadataDict['year'] = date[-4:]

        authors = isbn_data.get('authors', 'wat')
        metadataDict['authors'] = ' and '.join([author.get('name', '')
                                                for author in authors])

        # unlike worldcat, openlibrary does not provide edition information
        return metadataDict
    except:
        return None


# flagging
# you can only flag a listing once...
def can_flag(flagger, listing):
    user_flag_num = Flag.objects.filter(flagger=flagger,
                                        listing=listing).count()
    # we're assuming that this isn't going to go over 1
    if user_flag_num:
        return False
    else:
        return True


def can_flag_bid(flagger, bid):
    user_flag_num = BidFlag.objects.filter(flagger=flagger,
                                           bid=bid).count()
    if user_flag_num:
        return False
    else:
        return True


# get the listing's slug to pass to the create flag page
def flag_slug(flagger, listing):
    if not can_flag(flagger, listing):
        return Flag.objects.get(flagger=flagger, listing=listing).slug
    else:
        return None


def bid_flag_slug(flagger, bid):
    if not can_flag_bid(flagger, bid):
        return BidFlag.objects.get(flagger=flagger, bid=bid).slug
    else:
        return None


# rating
# (basically) duplicated code!!!
def can_rate(rater, listing):
    user_rate_num = Rating.objects.filter(rater=rater,
                                          listing=listing).count()
    # we're assuming that this isn't going to go over 1
    if user_rate_num:
        return False
    else:
        return True
