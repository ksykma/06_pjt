from django.db import models
from django.conf import settings

# Create your models here.
class Movie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MOEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    description = models.TextField()
    
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MOEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)