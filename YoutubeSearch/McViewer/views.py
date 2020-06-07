import requests

from isodate import parse_duration
from django.shortcuts import render, redirect

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import login, authenticate
from django.forms import ValidationError
from datetime import date
from django.contrib.auth.decorators import login_required

@login_required
def index(request, username):
    user_profile = UserProfile.objects.get(user=request.user)
    recent_searches = Search.objects.filter(user_profile=user_profile)
    return render(request, 'home_page.html', {
        'userProfile': user_profile,
        'recentSearches': recent_searches,
        'numOfSearches': len(recent_searches)
    })

def signUp(request):
    if request.method == "POST" and "submitProfile" in request.POST:
        the_first_name = request.POST.get("first_name")
        the_last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        the_email = request.POST.get("email")
        raw_password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            context = {'error':'The username you entered has already been taken. Please try another username.'}
            return render(request, 'sign_up.html', context)

        if User.objects.filter(email=the_email).exists():
            context = {'error':'The email you entered has already been taken. Please try another email.'}
            return render(request, 'sign_up.html', context)

        user = User.objects.create_user(username = username, first_name = the_first_name, last_name = the_last_name, email = the_email, password = raw_password)
        user.save()
        userprofile = UserProfile.objects.create(
            user = user,
        )
        userprofile.save()
        userAccount = authenticate(username=username, password=raw_password)
        login(request, userAccount)
        return redirect('home_page', username=username)
    return render(request, 'sign_up.html')
    
# def login(request):

#     return render(request, 'sign_in.html')

@login_required
def searchResult(request):

    if request.method == "GET":
        search = request.GET.get("search")
        user_profile = UserProfile.objects.get(user=request.user)

        videos = getSearchedVideos(search, 6)
        newSearch = Search.objects.create(
            text = search,
            date_searched = date.today(),
            user_profile = user_profile,
            title = videos[0]['title'],
            thumbnail = videos[0]['thumbnail']
        )
        newSearch.save()
        
        if Search.objects.filter(user_profile=user_profile).count() > 3:
            earliest_search = Search.objects.filter(user_profile=user_profile).order_by('id').first()
            earliest_search.delete()

        return render(request, 'search.html', {
            'search': newSearch,
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

@login_required
def editProfile(request):
    if request.method == "POST" and "editProfile" in request.POST:
        the_first_name = request.POST.get("first_name")
        the_last_name = request.POST.get("last_name")
        raw_password = request.POST.get("password")
        form = ImageUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            image = form.cleaned_data['image']
        
        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        user_profile.display_picture = image
        user.update(username = username, first_name = the_first_name, last_name = the_last_name, email = the_email, password = raw_password)
        user.save()
        user_profile.save()
        
        return redirect('home_page', username=username)
    return render(request, 'edit_profile.html')