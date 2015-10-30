from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.utils import timezone
from .models import Listing
from .forms import UserForm

# Create your views here.

# Defining the "base" view here.
# We want to incorporate our blog listings here, so we do a query on the model of Listing to get the objects.
def base(request):
	# We return a rendered index.html
	return render(request, 'blog/index.html', {})

# This is for registering a new account on the site.
def register(request):
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			username, password = form.cleaned_data['username'], form.cleaned_data['password']
			user = User.objects.create_user(username=username, password=password)
			user.is_active = True
			user.save()
			new_user = authenticate(username=username, password=password)
			login(request, new_user)
			return HttpResponseRedirect("/listing_list")
	else:
		form = UserForm()

	return render(request, 'blog/register.html', {'form': form})

def listing_list(request):
	listings = Listing.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/listing_list.html', {'listings': listings})

# For viewing a blog listing individually. We load the primary key of the listing from the database.
# Refer to the <a> tag inside listing_list.html 
def listing_detail(request, listing_id):
	listing = get_object_or_404(Listing, pk=listing_id)
	return render(request, 'blog/listing_detail.html', {'listing': listing})

def listing_new(request):
	return render(request, 'blog/listing_new.html')
