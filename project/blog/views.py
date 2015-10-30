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
			return HttpResponseRedirect("/post_list")
	else:
		form = UserForm()

	return render(request, 'blog/register.html', {'form': form})

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

# For viewing a blog post individually. We load the primary key of the post from the database.
# Refer to the <a> tag inside post_list.html 
def post_detail(request, post_id):
	post = get_object_or_404(Post, pk=post_id)
	return render(request, 'blog/post_detail.html', {'post': post})
