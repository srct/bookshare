from django.contrib import admin
from .models import Lookout

@admin.register(Lookout)
class LookoutAdmin(admin.ModelAdmin):
	list_display = ('id', 'created', 'modified', 'owner', 'isbn')
	list_filter = ('created', 'modified', 'owner')
