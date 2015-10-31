from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from .models import Listing
from .forms import UserForm, ListingForm

from django.views.generic import View
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin

# Create your views here.

# Defining our own Generic editing views for CRUD.
# ListingUpdate handles the updating of Listings
class ListingUpdate(UpdateView):
	model = Listing
	template_name = 'blog/listing_update.html'
	pk_url_kwarg = 'listing_id'
	fields = ['title', 'text']

	# Overriding UpdateView's base class' method, post, in order to provide our own CRUD authorization.
	def post(self, request, listing_id):
		# Set the object instance in case user cancels their delete request.
		# Must be called self.object since we are overriding the base class's self.object.
		self.object = get_object_or_404(Listing, pk=listing_id)
		if request.user == self.object.author:
			return super(ListingUpdate, self).post(request, listing_id)
		else:
			# Return to main page if user tries perform an unauthorized action.
			return HttpResponseRedirect("/")


class ListingDelete(DeleteView):
	model = Listing
	pk_url_kwarg = 'listing_id'
	success_url = reverse_lazy('listing_list')

	# Overriding DeleteView's base class' method, post, in order to provide our own CRUD authorization.
	def post(self, request, listing_id):
		# Set the object instance in case user cancels their delete request.
		# Must be called self.object since we are overriding the base class's self.object.
		self.object = get_object_or_404(Listing, pk=listing_id)
		if request.user == self.object.author:
			# "Cancel" refers to the tag <input name="Cancel" ...> from listing_confirm_delete.html
			if "Cancel" in request.POST:
				url = self.get_success_url()
				return HttpResponseRedirect(url)
			else:
				return super(ListingDelete, self).post(request, listing_id)
		else:
			# Return to main page if user tries perform an unauthorized action.
			return HttpResponseRedirect("/")

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
	if request.method == "POST":
		form = ListingForm(request.POST)
		if form.is_valid():
			title, text = form.cleaned_data['title'], form.cleaned_data['text']
			listing = Listing.objects.create(author=request.user, title=title, text=text)
			listing.publish()
			return HttpResponseRedirect("/listing_list")
	else:
		form = ListingForm()

	return render(request, 'blog/listing_new.html', {'form': form})
