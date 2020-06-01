import requests

from isodate import parse_duration

from django.shortcuts import render
from django.config import settings
from django.http import HttpResponse

def index(request):
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    search_params = {
        'part' : 'snippet',
        'q' : 'learn python',
        'key' : settings.YOUTUBE_API_KEY,
        'maxResults' : 9,
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
        'maxResults' : 9
    }
    res = requests.get(search_url, params = video_params)

    results = res.json()['items']

    videos = []
    for results in results:
        video_data = {
            'title' : result['snippet']['title'],
            'id' : result['id']
            'duration' : parse_duration(result['contentDetails']['duration'])
            'thumbnail' : result['snippet']['thumbnails']['high']['url']
        }
        videos.append(video_data)
    
    context = {
        'videos' : videos
    }

    return render(request, 'McViewer/login.html', context)
# Create your views here.
def login(request):
    return render(request, 'McViewer/login.html')
# Create your views here.

