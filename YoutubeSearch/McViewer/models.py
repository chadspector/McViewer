from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime

#Create your models here.
class Video(models.Model):
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
    title = models.CharField(max_length=255,default="None")
<<<<<<< HEAD
    duration = models.CharField(max_length=255,default="None")
=======
    duration = models.DurationField(default="None")
>>>>>>> origin/chad
    creator = models.CharField(max_length=255,default="None")
    link = models.CharField(max_length=255,default="None")
    description = models.CharField(max_length=1000,default="None")
    
class Search(models.Model):
    first_video = models.ForeignKey(Video, on_delete=models.CASCADE)
    date_searched = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=255,default="None")

class UserProfile(models.Model):
    display_picture = models.ImageField(upload_to='profile_images/', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True) 
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
