# core django imports
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
# third-part imports
import requests
# imports from your apps
from django.conf import settings
from .models import Student


def pfinfo(u_name):
    pf_url = settings.PF_URL
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
        user.set_password('cas_used_instead')
        print("Added user email and default password.")

        print "Start peoplefinder parsing"
        try:
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

        except Exception as e:
            print("Unhandled peoplefinder exception:", e)

        user.save()
        print("Created user %s!" % username)

    else:
        print("User object already exists.")


    # Student Creation Section
    try:
        Student.objects.get(user=user)
        print("Student object already exists")

    except ObjectDoesNotExist:
        new_student = Student.objects.create(user=user)

        # save the name off of peoplefinder for later quality assurance purposes
        new_student.pf_first_name = user.first_name
        new_student.pf_last_name = user.last_name

        new_student.save()
        print("Created student object for user %s!" % username)

    print("CAS callback completed.")
