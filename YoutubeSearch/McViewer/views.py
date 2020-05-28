from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return render(request, 'McViewer/login.html')
# Create your views here.
