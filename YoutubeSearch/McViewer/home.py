from django.shortcuts import render
from django.http import HttpResponse

def login(request):

    return render(request, 'sign_in.html', {
        
    })

def signIn(request):

    return render(request, 'sign_up.html', {
        
    })

def homeView(request):

    return render(request, 'home_page.html', {
        
    })