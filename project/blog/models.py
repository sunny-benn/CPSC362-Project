from django.db import models
from django.utils import timezone

# Create your models here.

# This models the Post object that we will use to create posts.
class Post(models.Model):
	# Each model has its own attributes.
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField(default=timezone.now)
	published_date = models.DateTimeField(blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title