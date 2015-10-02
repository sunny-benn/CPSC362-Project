from django.shortcuts import render
from django.utils import timezone
from .models import Post

# Create your views here.

# Defining the "base" view here.
# We want to incorporate our blog posts here, so we do a query on the model of Post to get the objects.
def base(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

	# We return a rendered base.html with our model "posts".
	return render(request, 'blog/base.html', {'posts': posts})

