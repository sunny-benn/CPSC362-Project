from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate, login
from .models import Post

# This is a for which defines our user accounts. 
class UserForm(forms.Form):
	username = forms.CharField(label='Username')
	password = forms.CharField(widget=forms.PasswordInput())

	error_messages = {
		'invalid_login': ("Login failed. Please enter a correct username and password. "
						   "Note that both fields may be case-sensitive."),
		'inactive': ("This account is inactive."),
	}

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'text')