from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from .views import ListingUpdate, ListingDelete

import notifications

# Each url pattern is tied to a view.
# If you check views.py, you'll notice that we are defining "base".
urlpatterns = [
	url(r'^$', views.base, name='base'),
	url(r'^about$', views.about, name='about'),
	url(r'^register$', views.register, name='register'),
    url(r'^listing_list$', views.listing_list, name='listing_list'),

    # Using Django's built-in login view.
	url(r'^login$', auth_views.login, {'template_name': 'blog/login.html'}, name='login'),
    
	# Here we pass Django's built-in logout view, then we redirect back to "base" view.
	url(r'^logout$', auth_views.logout, 
		{
			"next_page": reverse_lazy('base')
		}, name='logout'),

	# This is for viewing blog listings individually.
	url(r'^listing/(?P<listing_id>[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$', views.listing_detail, name='listing_detail'),
	url(r'^listing/new$', views.listing_new, name='listing_new'),
	url(r'^listing/delete/(?P<listing_id>[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$', ListingDelete.as_view(), name='listing_delete'),
	url(r'^listing/update/(?P<listing_id>[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$', ListingUpdate.as_view(), name='listing_update'),

	url(r'^search$', views.search, name='search'),

	# The following url patters are for the notifications feature.
	url(r'^inbox/notifications/', include(notifications.urls), name='notifications'),
	url(r'^inbox/notifications/mark-all-as-read$', views.mark_all_as_read, name='mark_all_as_read'),
	url(r'^get-interested-users$', views.get_interested_users, name='get_interested_users'),
	url(r'^send-notification$', views.send_notification, name='send_notification'),
	
	# Below is for the url of the pictures uploaded by users

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)