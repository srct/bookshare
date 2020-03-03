# core django imports
from django.contrib import admin
# imports from your apps
from .models import Student, Course

class StudentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created')

admin.site.register(Student, StudentAdmin)
admin.site.register(Course)
