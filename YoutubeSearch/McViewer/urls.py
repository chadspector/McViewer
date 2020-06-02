from django.contrib import admin
from django.urls import path, include
from . import home
from django.conf.urls.static import static


urlpatterns = [
    path('login', home.login, name="login"),
    path('sign_up', home.signUp, name="sign_up"),
    path('homepage', home.homeView, name="home_page")
]