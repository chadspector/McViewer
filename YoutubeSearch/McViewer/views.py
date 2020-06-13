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

#This method checks whether the user performing the request is authenticated.
#If they are authenticated, meaning they have signed up for McViewer, they are redirected to their homepage.
#If they are not authenticated, the welcome page is rendered where the user is give the opportunity to sign up.
def welcome(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    return render(request, "welcome.html")

#This method renders the user's dashboard upon sign-in. 
#The user's 3 most recent searches are displayed by filtering all Search objects attached to this specific user
#and then ordering them by how recent the Search objects were created.
@login_required(login_url='login')
def index(request):
    user_profile = UserProfile.objects.get(user=request.user)
    searches = Search.objects.filter(user_profile=user_profile).order_by('date_searched')
    recent_searches = reversed(searches)
    return render(request, 'home_page.html', {
        'userprofile': user_profile,
        'recentSearches': recent_searches,
        'numOfSearches': len(searches)
    })

#This method provides the sign-up logic for McViewer.
#Upon clicking the sign-up button, all of the user's inputs are received from the sign-up form.
#Input validation occurs by checking whether the email or username inputted by the user are already in use
#by filtering through all Users in the database and checking is any User has that particular username or email.
#If this is the case, the appropriate error message is displayed.
#If the input validation checks are passed, a User object is created, a UserProfile object is created, the user is 
#authenticated and logged in.
#Finally, the user is redirected to their dashboard.
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

#This method provides the sign-in logic for McViewer.
#Upon clicking the sign-up button, all of the user's inputs are received from the sign-in form.
#If a User with the inputted email exists, check that the inputted password matches that user's email.
#If the email and password match, log the user in and send the user to their ddashboard.
#If the email and password do not match, display an error message to the user telling them that they
#inputted the wrong password. The user is allowed to try a new password.
#If there is no User with the inputted email that exists, display an error message to the user telling
#them that they have inputted an invalid email. The user is allowed to try a new email.
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
    
#
@login_required(login_url='login')
def editProfile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    if request.method == "POST" and "editProfile" in request.POST:
        the_first_name = request.POST.get("first_name")
        the_last_name = request.POST.get("last_name")
        form = ImageUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            display_picture = form.cleaned_data['image']
            user_profile.display_picture = display_picture
        
        user.first_name = the_first_name
        user.last_name = the_last_name
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
    #try:
    if 1<2:
        network = PrivateNetwork.objects.get(referral_code = referral_code)
        unsorted_searches = []
        users = network.users.all()
        count = network.users.count()
        for user in users:
            for search in Search.objects.filter(user_profile=user):
                unsorted_searches.append(search)
        
        print("%#######")
        print(len(unsorted_searches))
        if len(unsorted_searches) > 1:
            searches_wrong_order = unsorted_searches.order_by('date_searched')[:6]
            searches = reversed(searches_wrong_order)
        else:
            searches = []
            for search in unsorted_searches:
                searches.add(search)
        return render(request, 'private_network.html', {
            'searches': searches,
            'network':network,
            'count':count,
            })
    #except:
     #   return redirect('network')