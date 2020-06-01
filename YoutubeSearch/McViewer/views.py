import requests

from isodate import parse_duration

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

def search(request):
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
    
    search_results = res.json()['items']
    for result in search_results:
        video_ids.append(result['id']['videoId'])
    
    
    video_params = {
        'key' : settings.YOUTUBE_API_KEY,
        'part' : 'snippet,contentDetails',
        'id' : ','.join(video_ids),
        'maxResults' : 6
    }
    res = requests.get(video_url, params = video_params)

    video_results = res.json()['items']

    videos = []
    for result in video_results:
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

    return render(request, 'home_page.html', context)
# Create your views here.
def login(request):
    return render(request, 'login.html')
# Create your views here.

