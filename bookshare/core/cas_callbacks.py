# core django imports
from django.conf import settings
from django.contrib.auth.models import User
# third-part imports
import requests
# imports from your apps
from .models import Student


def pfinfo(u_name):
    pf_url = "http://peoplefinder.b1.akshaykarthik.com/"
    url = str(pf_url) + "basic/all/" + str(u_name)
    try:
        metadata = requests.get(url)
        metadata.raise_for_status()
    except requests.exceptions.RequestException as e:
        print e
    else:
        pf_json = metadata.json()
        try:
            name = pf_json['results'][0]['name']
            return name.split(',')
        # if the name is not in peoplefinder, return empty first and last name
        except IndexError:
            return ['', '']


def create_user(tree):
    username = tree[0][0].text
    print username
    user, user_created = User.objects.get_or_create(username=username)

    if user_created:
        user.email = "%s@%s" % (username, settings.ORGANIZATION_EMAIL_DOMAIN)
        print "hello"
        name_list = pfinfo(str(username))
        print name_list, "name_list"
        first_name = name_list[1].lstrip().split(' ')
        if len(first_name) > 1:
            no_mi = first_name[:-1]
            user.first_name = ' '.join(no_mi)
        else:
            user.first_name = ' '.join(first_name)
        last_name = name_list[0]
        user.last_name = name_list[0]

        print "world"
        user.save()
        new_student = Student.objects.create(user=user)
        new_student.save()

        print("Created user %s!" % username)
