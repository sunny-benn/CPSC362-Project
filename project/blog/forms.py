from django import forms

# This is a for which defines our user accounts. 
class UserForm(forms.Form):
	username = forms.CharField(label='Username')
	password = forms.CharField(widget=forms.PasswordInput())