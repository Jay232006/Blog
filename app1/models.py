from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    VISIBILITY_CHOICES = [('public', 'Public'), ('private', 'Private')]

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=100)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    #like feature
    liked_by = models.ManyToManyField(User, related_name='liked_blogs', blank=True)
    def __str__(self):
        return self.title
