from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.utils import timezone
from .models import Post
from .forms import UserForm

# Create your views here.

# Defining the "base" view here.
# We want to incorporate our blog posts here, so we do a query on the model of Post to get the objects.
def base(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

	# If the user is initiating POST then we give them the form.
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			username, password = form.cleaned_data['username'], form.cleaned_data['password']
			new_user = authenticate(username=username, password=password)
			if new_user:
				login(request, new_user)
				return HttpResponseRedirect("/")
			else:
				# When the user does not type the correct credentials, display error.
				# This is part is not complete.
				# TODO: 
				pass
			
	else:
		form = UserForm()
			
	# We return a rendered base.html with our model "posts".
	return render(request, 'blog/base.html', {'posts': posts, 'user_logged_in': request.user.is_authenticated(), 'form': form})

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
			return HttpResponseRedirect("/")
	else:
		form = UserForm()

	return render(request, 'blog/register.html', {'form': form})

# For viewing a blog post individually. We load the primary key of the post from the database.
# Refer to the <a> tag inside post_list.html 
def post_detail(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	return render(request, 'blog/post_detail.html', {'post': post})
