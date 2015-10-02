from django.conf.urls import url
from . import views

# Each url pattern is tied to a view.
# If you check views.py, you'll notice that we are defining "base".
urlpatterns = [
	url(r'^$', views.base, name='base'),
]