# core django imports
from django.contrib import admin
# imports from your apps
from .models import Student, Course

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created')

admin.site.register(Course)
