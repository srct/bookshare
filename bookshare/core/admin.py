# core django imports
from django.contrib import admin
# imports from your apps
from .models import Student, Course

admin.site.register(Student)
admin.site.register(Course)
