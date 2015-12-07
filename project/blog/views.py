import os
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone

from .models import Listing, ListingPicture
from .forms import UserForm, ListingForm, ListingPictureForm
from django.forms import modelformset_factory

from django.forms.models import model_to_dict

from django.views.generic import View
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin

from django.core.files.uploadedfile import InMemoryUploadedFile

from django.db.models import Q

from notifications import notify

# This function takes a formset, cleans it, enumerates it, and saves the corresponding object to the database. 
# This function is not a view; just providing a service.
def savePictureFormToDB(pictureFormSet, listing):
	# Get data from the form
	cleaned_data = pictureFormSet.cleaned_data
	print("cleaned_data:", cleaned_data)

	# For each picture the user uploads, create a corresponding ListingPicture object
	for index, pic in enumerate(pictureFormSet):
		# If the form is empty, break out of this loop.
		if cleaned_data[index] == {}:
			break

		clean_pic = cleaned_data[index]['picture']
		clean_id = cleaned_data[index]['id']

		# If the user checked the "Clear" check-box, delete the image.
		if clean_pic == False:
			os.remove(clean_id.picture.path)
			clean_id.delete()
		
		# This checks if the image is the one that was uploaded (instance of InMemoryUploadedFile). 
		# If we do not have this check, we will create duplicates,
		# since the code will add every image from the form (including existing ones).
		# Images that have already been uploaded are instances of ImageFieldFile.
		elif not isinstance(clean_pic, InMemoryUploadedFile):
			continue

		# If the image is an instance of InMemoryUploadedFile, save to DB.
		else:
			picture = ListingPicture.objects.create(picture=clean_pic, picture_id=listing)
			picture.save()
	return

# Defining a generic editing views for handling when the user wants to edit/update their listing.
class ListingUpdate(UpdateView):
	model = Listing
	template_name = 'blog/listing_update.html'
	pk_url_kwarg = 'listing_id'
	fields = ['title', 'price', 'text']

	# Here we are instantiating a formset with ListingPictureForm.
	ListingPictureFormSet = modelformset_factory(ListingPicture, form=ListingPictureForm, extra=5, max_num=5)
	pictureFormSet = None

	# Overriding UpdateView's post() method in order to provide our own implementation.
	def post(self, request, listing_id):
		# Initializing formset with existing pictures from the listing (queryset).
		pictureFormSet = self.ListingPictureFormSet(request.POST, request.FILES, queryset=ListingPicture.objects.filter(picture_id=listing_id))

		# Set the object instance in case user cancels their delete request.
		# Must be called self.object since we are overriding the UpdateView's self.object.
		self.object = get_object_or_404(Listing, pk=listing_id)
		if request.user == self.object.author:
			# Save updated picture form to database if there's been a change
			if pictureFormSet.is_valid() and pictureFormSet.has_changed():
				print("valid and has changed")
				savePictureFormToDB(pictureFormSet, self.object)
			else:
				print("errors:", pictureFormSet.errors)
			return super(ListingUpdate, self).post(request, listing_id)
		else:
			# Return to main page if user tries perform an unauthorized action.
			return HttpResponseRedirect("/")

	# Overriding UpdateView's get_context_data() method in order to include the formset in the template.
	def get_context_data(self, **kwargs):
		# Get context object from UpdateView.
		context = super(ListingUpdate, self).get_context_data(**kwargs)
		try:
			# Build a picture formset based on the listing the user is editing. 
			pictureFormSet = self.ListingPictureFormSet(queryset=ListingPicture.objects.filter(picture_id=context['listing'].key))
			# Pass it to the context object so it's accessible to the template.
			# This is equivalent to render(request, <template path>, {'pictures': pictureFormSet})
			context['pictures'] = pictureFormSet
		except Exception as e:
			context['pictures'] = None
		return context

# Defining a generic delete views for handling when the user wants to delete their listing.
class ListingDelete(DeleteView):
	model = Listing
	pk_url_kwarg = 'listing_id'
	success_url = reverse_lazy('listing_list')

	# Overriding DeleteView's post() in order to provide our own implementation.
	def post(self, request, listing_id):
		# Set the object instance in case user cancels their delete request.
		# Must be called self.object since we are overriding the DeleteView's self.object.
		self.object = get_object_or_404(Listing, pk=listing_id)
		if request.user == self.object.author:
			# "Cancel" refers to the tag <input name="Cancel" ...> from the template listing_confirm_delete.html
			if "Cancel" in request.POST:
				url = self.get_success_url()
				return HttpResponseRedirect(url)
			else:
				return super(ListingDelete, self).post(request, listing_id)
		else:
			# Return to main page if user tries perform an unauthorized action.
			return HttpResponseRedirect("/")

# Defining the base view here. Basic homepage.
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

# When the user clicks the "Browse" button in the navbar.
def listing_list(request):
	listings = Listing.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/listing_list.html', {'listings': listings})

# For viewing a listing individually. We load the primary key of the listing from the database.
# Refer to the <a> tag inside listing_list.html 
def listing_detail(request, listing_id):
	listing = get_object_or_404(Listing, pk=listing_id)
	pictures = ListingPicture.objects.filter(picture_id=listing_id)
	return render(request, 'blog/listing_detail.html', {'listing': listing, 'pictures': pictures})

# For creating a new listing.
def listing_new(request):
	ListingPictureFormSet = modelformset_factory(ListingPicture, form=ListingPictureForm, extra=5, max_num=5)

	if request.method == "POST":
		form = ListingForm(request.POST)
		pictureFormSet = ListingPictureFormSet(request.POST, request.FILES, queryset=ListingPicture.objects.none())

		if form.is_valid():
			title, text, price = form.cleaned_data['title'], form.cleaned_data['text'], form.cleaned_data['price']
			listing = Listing.objects.create(author=request.user, title=title, text=text, price=price)
			listing.publish()

			if pictureFormSet.is_valid():
				savePictureFormToDB(pictureFormSet, listing)

			return HttpResponseRedirect("/listing_list")
	else:
		form = ListingForm()
		pictureFormSet = ListingPictureFormSet(queryset=ListingPicture.objects.none())

	return render(request, 'blog/listing_new.html', {'form': form, 'pictureFormSet': pictureFormSet})

# This view is for handling the search queries.
# Utilizing Q objects provided by Django:
# https://docs.djangoproject.com/en/1.8/topics/db/queries/#complex-lookups-with-q-objects
def search(request):
	if request.method == "GET":	
		query = request.GET.get('search_box', None)
		results = Listing.objects.filter(
				Q(title__contains=query) | Q(text__contains=query),
				published_date__lte=timezone.now()
			).order_by('published_date')
		
		# Return results to already created listing_list template; no need to have an extra template.
		return render(request, 'blog/listing_list.html', {'listings': results})

# Marks all user's notifications as read; redirects to current page.
def mark_all_as_read(request):
	request.user.notifications.mark_all_as_read()

	return HttpResponseRedirect(request.META['HTTP_REFERER'])

# AJAX View to return the list of users who are interested in the listing.
def get_interested_users(request):
	# Make sure the request is AJAX and POST
	if request.is_ajax() and request.method == 'POST':
		if 'listingID' in request.POST:
			try:
				unread_list = []

				for n in request.user.notifications.unread().filter(action_object_object_id=request.POST['listingID']):
					struct = model_to_dict(n)
					if n.actor:
						struct['actor'] = str(n.actor)
					
					struct['description'] = "User " + struct['actor'] + " is interested"

					unread_list.append(struct)

				data = {
					'response': 'success',
					'unread_list':unread_list
				}

				return JsonResponse(data)
			except Exception as e:
				print(e)
				data = {
					'response': 'fail',
				}
				return JsonResponse(data)
	
	return JsonResponse({'response': 'fail'})



# AJAX View to send a notification to the author of the listing when a user click the "I'm Interested" button.
def send_notification(request):
	# Make sure the request is AJAX and POST
	if request.is_ajax() and request.method == 'POST':
		if 'listingID' in request.POST:
			try:
				listing = get_object_or_404(Listing, pk=request.POST['listingID'])
				notify.send(request.user, recipient=listing.author, verb='is interested in', action_object=listing)
			except Exception as e:
				print(e)
				return HttpResponse('fail')

			return HttpResponse('success')
	return HttpResponse('fail')
