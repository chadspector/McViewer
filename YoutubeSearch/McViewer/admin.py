from django.contrib import admin
from .models import UserProfile, Video, Search

admin.site.register(UserProfile)
admin.site.register(Video)
admin.site.register(Search)
# Register your models here.
