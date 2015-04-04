from django.contrib.auth.models import User
from django.conf import settings

from .models import Student

import requests

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
        name = pf_json['results'][0]['name']
        return name.split(',')

def create_user(tree):

    username = tree[0][0].text
    print username
    user, user_created = User.objects.get_or_create(username=username)

    if user_created:
        user.email = "%s@%s" % (username, settings.ORGANIZATION_EMAIL_DOMAIN)
#        print "hello"
#        name_list = pfinfo(str(username))
#        print "world"
#        user.first_name = name_list[1].rstrip()
#        print "something"
#        user.last_name = name_list[0]
        user.save()
        new_student = Student.objects.create(user=user)
        new_student.save()

        print("Created user %s!" % username)
