from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Organization, Listing, VolunteerInterest


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('display_name',)


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('name',)


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('listing_type', 'kind', 'category', 'title', 'description', 'price', 'is_volunteer', 'location')
