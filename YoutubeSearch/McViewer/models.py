from django.db import models
from django.contrib.auth.models import User

#Create your models here.

class Video(models.Model):
    user = models.ManyToManyField(User, null=0, default="None")