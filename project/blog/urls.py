from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

# Each url pattern is tied to a view.
# If you check views.py, you'll notice that we are defining "base".
urlpatterns = [
	url(r'^$', views.base, name='base'),
	url(r'^register$', views.register, name='register'),
    url(r'^post_list$', views.post_list, name='post_list'),

    # Using Django's built-in login view.
	url(r'^login$', auth_views.login, {'template_name': 'blog/login.html'}, name='login'),
    
	# Here we pass Django's built-in logout view, then we redirect back to "base" view.
	url(r'^logout$', auth_views.logout, 
		{
			"next_page": reverse_lazy('base')
		}, name='logout'),

	# This is for viewing blog posts individually.
	url(r'^post/(?P<post_id>[0-9]+)$', views.post_detail, name='post_detail'),
	url(r'^post/new$', views.post_new, name='post_new'),
]