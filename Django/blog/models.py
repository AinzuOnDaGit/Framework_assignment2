from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=100)
    image_filename = models.CharField(max_length=100, null=True, blank=True)

# Django recommends defining __str__, provides human-readable representation of the model instance.
# improves debugging throughout Django admin interface.
    def __str__(self):
        return self.post.title
