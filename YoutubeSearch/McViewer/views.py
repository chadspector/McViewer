import requests
from isodate import parse_duration
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import UserProfile, Search, Video
from django.forms import ValidationError 

def index(request, username):
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    search_params = {
        'part' : 'snippet',
        'q' : 'learn python',
        'key' : settings.YOUTUBE_API_KEY,
        'maxResults' : 6,
        'type' : 'video'
    }
    video_ids = []
    res = requests.get(search_url, params = search_params)
    
    results = res.json()['items']

    for result in results:
        video_ids.append(result['id']['videoId'])    

    video_params = {
        'key' : settings.YOUTUBE_API_KEY,
        'part' : 'snippet,contentDetails',
        'id' : ','.join(video_ids),
        'maxResults' : 6
    }
    res = requests.get(search_url, params = video_params)

    results = res.json()['items']

    videos = []
    for result in results:
        video_data = {
            'title' : result['snippet']['title'],
            'id' : result['id'],
            'duration' : parse_duration(result['contentDetails']['duration']),
            'thumbnail' : result['snippet']['thumbnails']['high']['url']
        }
        videos.append(video_data)
    
    context = {
        'videos' : videos
    }

    return render(request, 'McViewer/login.html', context)
# Create your views here.

def signUp(request):
    if request.method == "POST" and "submitProfile" in request.POST:
        the_first_name = request.POST.get("first_name")
        the_last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        the_email = request.POST.get("email")
        raw_password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("This username already exists."))

        if User.objects.filter(email=the_email).exists():
            raise forms.ValidationError(_("This email already exists."))

        user = User.objects.create_user(username, first_name = the_first_name, last_name = the_last_name, email = the_email, password = raw_password)
        user.save()
        userprofile = UserProfile.objects.create(
            user = user,
        )
        userprofile.save()
        return redirect('home_page', username = username)

    return render(request, 'sign_up.html')
def login(request):
    
    return render(request, 'sign_in.html')

def searchResult(request):
    
    return render(request, 'search.html')
