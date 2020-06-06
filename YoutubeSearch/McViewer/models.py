from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class UserProfile(models.Model):
    display_picture = models.ImageField(upload_to='images', default="default.jpg")
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Search(models.Model):
    date_searched = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=255,default="None")
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255,default="None")
    thumbnail = models.ImageField(default='default.jpg', upload_to='images')

