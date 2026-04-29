from django.contrib import admin
from .models import Profile, UserProfile, Organization, VolunteerInterest, Listing, Connection

admin.site.register(Profile)
admin.site.register(UserProfile)
admin.site.register(Organization)
admin.site.register(VolunteerInterest)
admin.site.register(Listing)
admin.site.register(Connection)
