# standard library imports
from __future__ import absolute_import, print_function
# core django imports
from django.conf import settings
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
# third-part imports
import requests
# imports from your apps
from .models import Student


def pfinfo(u_name):
    pf_url = settings.PF_URL
    url = str(pf_url) + "basic/all/" + str(u_name)
    try:
        metadata = requests.get(url, timeout=5)
        print("Retrieving information from the peoplefinder api.")
        metadata.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Cannot resolve to peoplefinder api:" , e)
    else:
        try:
            pf_json = metadata.json()
            name = pf_json['results'][0]['name']
            return name.split(',')
        # if the name is not in peoplefinder, return empty first and last name
        except IndexError:
            return ['', '']


def create_user(tree):

    print("Parsing CAS information.")
    try:
        username = tree[0][0].text
        user, user_created = User.objects.get_or_create(username=username)

        if user_created:
            print("Created user object %s." % username)
            user.email = "%s@%s" % (username, settings.ORGANIZATION_EMAIL_DOMAIN)
            user.set_password('cas_used_instead')

            try:
                name_list = pfinfo(str(username))
                first_name = name_list[1].lstrip().split(' ')
                if len(first_name) > 1:
                    no_mi = first_name[:-1]  # no middle initial
                    user.first_name = ' '.join(no_mi)
                else:
                    user.first_name = ' '.join(first_name)
                last_name = name_list[0]
                user.last_name = name_list[0]
                print("Added user's name, %s %s." % first_name, last_name)
            except:
                print("Problem setting user's name via peoplefinder.")

            user.save()
            print("User object creation completed.")

        else:
            print("User object already exists.")

        try:
            Student.objects.get(user=user)
            print("Student object already exists.")
        except ObjectDoesNotExist:
            new_student = Student.objects.create(user=user)
            new_student.save()
            print("Student object creation completed.")

        print("CAS callback successful.")

    except Exception as e:
        print("Unhandled user creation error:", e)
        # mail the administrators
