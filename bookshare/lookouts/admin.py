# core django imports
from django.contrib import admin
# imports from your apps
from .models import Lookout


@admin.register(Lookout)
class LookoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'modified', 'owner', 'isbn')
    list_filter = ('created', 'modified', 'owner')
