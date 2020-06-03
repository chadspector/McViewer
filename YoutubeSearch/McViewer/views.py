import requests
from isodate import parse_duration
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

def index(request):
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

    for results in results:
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
    for results in results:
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
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("user_name")
        password = request.POST.get("password")

        User.objects.create_user(username)

def login(request):
    
    return render(request, 'sign_in.html')

def signUp(request):
    
    return render(request, 'sign_up.html')

def searchResult(request):
    
    return render(request, 'search.html')



