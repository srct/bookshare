from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.forms import CheckboxSelectMultiple
from website.models import Listing, Seller

admin.site.register(Listing)
admin.site.register(Seller)

#class OrgInlinePerson(admin.StackedInline):
#    model = Organization.people.through
#    extra = 1
#    verbose_name = "Members"
#
#class OrgInlineAdmin(admin.StackedInline):
#    model = Organization.admins.through
#    extra = 1
#    verbose_name = "Admins"
#
#class PersonInlineOrg(admin.StackedInline):
#    model = Person.organizations.through
#    extra = 1
#    verbose_name = "Organizations"
#
#class PersonInlineTag(admin.StackedInline):
#    model = Person.tags.through
#    extra = 1
#    verbose_name = "Tags"
#
#class OpportunityInlineTag(admin.StackedInline):
#    model = Opportunity.tags.through
#    extra = 1
#    verbose_name = "Tags"
#
#class OpportunityInlineOrg(admin.StackedInline):
#    model = Opportunity.organizations.through
#    extra = 1
#    verbose_name = "Organization"
#
#class OpportunityInlinePerson(admin.StackedInline):
#    model = Opportunity.attendees.through
#    extra = 1
#    verbose_name = "Attendees"
#
#class TagAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None,          {'fields': ['name', 'description']})
#    ]
#    list_display = ('name', 'description')
#
#class PersonAdmin(admin.StackedInline):
#    model = Person
#    can_delete = False
#    fieldsets = [
#        (None,                   {'fields': ['description', 'maxdistance']}),
#        ("Location information", {'fields': ['city', 'state', 'country']}),
#	("Availability", {'fields': ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']})
#    ]
#    inlines = [PersonInlineOrg, PersonInlineTag]
#    form = AvailabilityandPictureForm
#
#class OrganizationAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None,		{'fields': ['name', 'description']}),
#	("Location information", {'fields': ['city', 'state', 'country']})
#    ]
#    inlines = [OrgInlinePerson, OrgInlineAdmin]
#    list_display = ('name', 'description')
#    form = PictureForm
#
#class OpportunityAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None,          {'fields': ['name', 'description']}),
#        ("Location information", {'fields': ['city', 'state', 'country']}),
#	("Times", {'fields': ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']})
#    ]
#    inlines = [OpportunityInlineTag, OpportunityInlineOrg, OpportunityInlinePerson]
#    list_display = ('name', 'description')
#    list_filter = ('name', 'tags', 'date_created')
#    form = AvailabilityForm
#
#class UserAdmin(UserAdmin):
#    inlines = (PersonAdmin,)
#
#admin.site.unregister(User)
#admin.site.register(Tag, TagAdmin)
#admin.site.register(User, UserAdmin)
#admin.site.register(Organization, OrganizationAdmin)
#admin.site.register(Opportunity, OpportunityAdmin)
