from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse_lazy, reverse
import uuid

# Create your models here.

# This models the Listing object that we will use to create listings.
class Listing(models.Model):
	# Each model has its own attributes.
	key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def get_absolute_url(self):
		return reverse('blog.views.listing_detail', args=[str(self.key)])

	def __str__(self):
		return self.title