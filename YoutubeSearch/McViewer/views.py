import requests
from isodate import parse_duration
from django.shortcuts import render, redirect

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import login, authenticate, logout
from django.forms import ValidationError
from datetime import date
from .forms import *
from django.contrib.auth.decorators import login_required


def welcome(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    return render(request, "welcome.html")

@login_required(login_url='login')
def index(request):
    user_profile = UserProfile.objects.get(user=request.user)
    searches = Search.objects.filter(user_profile=user_profile).order_by('date_searched')
    recent_searches = reversed(searches)
    if request.method == "POST" and "logout" in request.POST:
        logout(request)
        return redirect('login')
    return render(request, 'home_page.html', {
        'userprofile': user_profile,
        'recentSearches': recent_searches,
        'numOfSearches': len(searches)
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

        elif User.objects.filter(email=the_email).exists():
            context = {'error':'The email you entered has already been taken. Please try another email.'}
            return render(request, 'sign_up.html', context)

        user = User.objects.create_user(username = username, first_name = the_first_name, last_name = the_last_name, email = the_email, password = raw_password)
        userprofile = UserProfile.objects.create(
            user = user,
        )
        userAccount = authenticate(username=username, password=raw_password)
        login(request, userAccount)
        return redirect('home_page')
    return render(request, 'sign_up.html')

def loginprofile(request):
    if request.method == "POST" and "login" in request.POST:
        the_email = request.POST.get("email")
        raw_password = request.POST.get("password")
        if User.objects.filter(email = the_email).exists():
            user = User.objects.get(email = the_email)
            if user.check_password(raw_password) and user.is_authenticated:
                login(request, user)
                return redirect('home_page')
            else:
                context = {'error':'You have entered an invalid password.'}
                return render(request, 'sign_in.html', context)
        else:   
            context = {'error':'You have entered an invalid email.'}
            return render(request, 'sign_in.html', context)

    logout(request)
    return render(request, 'sign_in.html')

@login_required(login_url='login')
def searchResult(request):
    try:
        if request.method == "GET":
            search = request.GET.get("search")
            user_profile = UserProfile.objects.get(user=request.user)

            videos = getSearchedVideos(search, 7)
            
            if Search.objects.filter(user_profile=user_profile, title=videos[0]['title']).exists():
                newSearch = Search.objects.get(user_profile=user_profile, title=videoDisplayed['title'])
                newSearch.text = videoDisplayed['title']
                newSearch.date_searched = date.today()
            elif Search.objects.filter(user_profile=user_profile, text=videos[0]['title']).exists():
                newSearch = Search.objects.get(user_profile=user_profile, text=videoDisplayed['title'])
                newSearch.title = videoDisplayed['title']
                newSearch.date_searched = date.today()
            else: 
                newSearch = Search.objects.create(
                    text = search,
                    date_searched = date.today(),
                    user_profile = user_profile,
                    title = videos[0]['title'],
                    video_id = videos[0]['id'],
                    thumbnail = videos[0]['thumbnail']
                )
            
                if Search.objects.filter(user_profile=user_profile).count() > 3:
                    earliest_search = Search.objects.filter(user_profile=user_profile).order_by('id').first()
                    earliest_search.delete()
            newSearch.save()

            return render(request, 'search.html', {
                'search': newSearch,
                'videoDisplayed': videos[0],
                'upNextVideos' : videos[1:]
                })
    except:
        return redirect('home_page')
    
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

@login_required(login_url='login')
def getRelatedSearch(request, id):
    try:    
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        
        related_params = {
            'part' : 'snippet',
            'key' : settings.YOUTUBE_API_KEY,
            'maxResults' : 6,
            'relatedToVideoId' : id,
            'type' : 'video'
        }
        video_ids = []
        res = requests.get(search_url, params = related_params)
            
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

        related_results = res.json()['items']

        videos = []
        for result in related_results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'duration' : parse_duration(result['contentDetails']['duration']),
                'thumbnail' : result['snippet']['thumbnails']['high']['url']
            }
            videos.append(video_data)
        
        videoDisplayed_params = {
            'key' : settings.YOUTUBE_API_KEY,
            'part' : 'snippet,contentDetails',
            'id' : id,
        }
        res = requests.get(video_url, params = videoDisplayed_params)

        video_results = res.json()['items']

        videoDisplayed = video_results[0]

        videoDisplayed = {
            'title' : videoDisplayed['snippet']['title'],
            'id' : videoDisplayed['id'],
            'duration' : parse_duration(videoDisplayed['contentDetails']['duration']),
            'thumbnail' : videoDisplayed['snippet']['thumbnails']['high']['url']
        }

        user_profile = UserProfile.objects.get(user=request.user)

        if Search.objects.filter(user_profile=user_profile, title=videoDisplayed['title']).exists():
            newSearch = Search.objects.get(user_profile=user_profile, title=videoDisplayed['title'])
            newSearch.text = videoDisplayed['title']
            newSearch.date_searched = date.today()
        elif Search.objects.filter(user_profile=user_profile, text=videoDisplayed['title']).exists():
            newSearch = Search.objects.get(user_profile=user_profile, text=videoDisplayed['title'])
            newSearch.title = videoDisplayed['title']
            newSearch.date_searched = date.today()
        else:
            newSearch = Search.objects.create(
                text = videoDisplayed['title'],
                date_searched = date.today(),
                user_profile = user_profile,
                title = videoDisplayed['title'],
                video_id = videoDisplayed['id'],
                thumbnail = videoDisplayed['thumbnail']
            )
            if Search.objects.filter(user_profile=user_profile).count() > 3:
                earliest_search = Search.objects.filter(user_profile=user_profile).order_by('id').first()
                earliest_search.delete()
        newSearch.save()

        return render(request, 'search.html', {
            'search': videoDisplayed['title'],
            'videoDisplayed': videoDisplayed,
            'upNextVideos' : videos
            })
    except:
        return redirect('home_page')
    

@login_required(login_url='login')
def editProfile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if request.method == "POST" and "editProfile" in request.POST:
        the_first_name = request.POST.get("first_name")
        the_last_name = request.POST.get("last_name")
        new_email = request.POST.get("email")

        if User.objects.filter(email=new_email).exists():
            context = {'error':'The email you entered has already been taken. Please try another email.'}
            return render(request, 'edit_profile.html', context)

        form = ImageUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            display_picture = form.cleaned_data['image']
            user_profile.display_picture = display_picture
        
        user.first_name = the_first_name
        user.last_name = the_last_name
        user.email = new_email
        user.save()
        user_profile.save()
        return redirect('home_page')
    return render(request, 'edit_profile.html')

@login_required(login_url='login')
def network(request):
    searches_wrong_order = Search.objects.all().order_by('date_searched')[:6]
    searches = reversed(searches_wrong_order)
    count = UserProfile.objects.all().count()
    user_profile = UserProfile.objects.get(user = request.user)
    if request.method == "POST" and "join_network" in request.POST:
        the_referral_code = request.POST.get("code")
        if PrivateNetwork.objects.filter(referral_code = the_referral_code).exists():
            private_network = PrivateNetwork.objects.get(referral_code = the_referral_code)
            if user_profile in private_network.users.all():
                return render(request, 'public_network.html', {
                'error':'You are already part of this private network.',
                'searches':searches,
            })
            else:   
                private_network.users.add(user_profile)
                private_network.save()
                return redirect('private_network', referral_code = the_referral_code)
        else:
            return render(request, 'public_network.html', {
                'error':'A private network with this referral code does not exist.',
                'searches':searches,
            })

    elif request.method == "POST" and "create_network" in request.POST:
        return redirect('create_network')

    return render(request, 'public_network.html', {
        'searches': searches,
        'count':count,
        })

@login_required(login_url='login')
def createNetwork(request):
    user_profile = UserProfile.objects.get(user = request.user)
    if request.method == "POST" and "createNetwork" in request.POST:
        the_referral_code = request.POST.get("referral-code")
        the_name = request.POST.get("network_name")
        if PrivateNetwork.objects.filter(referral_code = the_referral_code).exists():
            return render(request, 'create_network.html', {
                'error':'A private network with this referral code already exists.',
            })
        else:
            private_network = PrivateNetwork.objects.create(title = the_name, date_created = date.today(), referral_code = the_referral_code)
            private_network.users.add(user_profile)
            private_network.save()
            return redirect('private_network', referral_code = the_referral_code)
    return render(request, 'create_network.html')

@login_required(login_url='login')
def privateNetwork(request, referral_code):
    try:
        network = PrivateNetwork.objects.get(referral_code = referral_code)
        unsorted_searches = []
        users = network.users.all()
        count = network.users.count()
        for user in users:
            for search in Search.objects.filter(user_profile=user):
                unsorted_searches.append(search)
        searches_wrong_order = unsorted_searches.order_by('date_searched')[:6]
        searches = reversed(searches_wrong_order)
        return render(request, 'private_network.html', {
            'searches': searches,
            'network':network,
            'count':count,
            })
    except:
        return redirect('network')