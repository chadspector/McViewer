import requests

from isodate import parse_duration
from django.shortcuts import render, redirect

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from django.forms import ValidationError
from datetime import date

def index(request, username):
    user=UserProfile.objects.get(user=request.user)
    return render(request, 'home_page.html', {
        "userProfile":user
    })

def signUp(request):
    if request.method == "POST" and "submitProfile" in request.POST:
       

        if User.objects.filter(username=username).exists():
            #raise ValidationError("This username already exists.")
            context = {'error':'The username you entered has already been taken. Please try another username.'}
            return render(request, 'sign_up.html', context)

        if User.objects.filter(email=the_email).exists():
            raise ValidationError("This email already exists.")

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

    if request.method == "GET":
        search = request.GET.get("search")
        user_profile = UserProfile.objects.get(user=request.user)
        newSearch = Search.objects.create(
            text = search,
            date_searched = date.today(),
            user_profile = user_profile
        )
        newSearch.save()
        if Search.objects.filter(user_profile=user_profile).count() > 3:
            earliest_search = Search.objects.filter(user_profile=user_profile).order_by('id').first()
            earliest_search.delete()

        videos = getSearchedVideos(search, 6)
        
        # context = {
        #     'videoDisplayed': videos[0],
        #     'upNextVideos' : videos[1:]
        # }
        
        return render(request, 'search.html', {
            "search":newSearch,
            'videoDisplayed': videos[0],
            'upNextVideos' : videos[1:]
        })
        
def getSearchedVideos(search, numResults):
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    search_params = {
            'part' : 'snippet',
            'q' : search,
            'key' : settings.YOUTUBE_API_KEY,
            'maxResults' : numResults,
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
        'maxResults' : numResults
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
    return videos