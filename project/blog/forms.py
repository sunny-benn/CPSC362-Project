from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate, login
from .models import Listing, ListingPicture

# This is a form which defines the fields the user sees when registering/logging in. 
class UserForm(forms.Form):
	username = forms.CharField(label='Username')
	password = forms.CharField(widget=forms.PasswordInput())

	error_messages = {
		'invalid_login': ("Login failed. Please enter a correct username and password. "
						   "Note that both fields may be case-sensitive."),
		'inactive': ("This account is inactive."),
	}

class ListingForm(forms.ModelForm):
	class Meta:
		model = Listing
		fields = ('title', 'price', 'text', )

class ListingPictureForm(forms.ModelForm):
	class Meta:
		model = ListingPicture
		fields = ('picture', )

		