from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate, login
from .models import Listing, ListingPicture

from django.contrib.auth.models import User

from decimal import *

# This is a form which defines the fields the user sees when registering/logging in. 
class UserForm(forms.Form):
	username = forms.CharField(label='Username')
	password = forms.CharField(widget=forms.PasswordInput())

	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError("That username is already taken")
		return username

class ListingForm(forms.ModelForm):
	class Meta:
		model = Listing
		fields = ('title', 'price', 'text', )

	def clean_price(self):
		price = self.cleaned_data['price']
		if price < Decimal('0.00'):
			raise forms.ValidationError("Price cannot be negative")
		return price

class ListingPictureForm(forms.ModelForm):
	class Meta:
		model = ListingPicture
		fields = ('picture', )

		