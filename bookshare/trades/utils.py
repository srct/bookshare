import requests
from .models import Flag, Rating, BidFlag


# pulls worldcat metadata from ISBNs
def ISBNMetadata(standardISBN):
    # passing in numbers starting with 0 throws "SyntaxError: invalid token"
    url = "http://xisbn.worldcat.org/webservices/xid/isbn/" +\
          str(standardISBN) +\
          "?method=getMetadata&format=json&fl=title,year,author,ed"

    # In case the API fails to return, simply return None.
    try:
        metadata = requests.get(url, timeout=3)
    except requests.ConnectionError:
        return None

    # format into a dictionary
    dejson = metadata.json()
    try:
        metadataDict = dejson.get('list')
        return metadataDict[0]
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
