from django.contrib import admin
from django.urls import path, include
from . import home
from django.conf.urls.static import static
<<<<<<< HEAD
from django.conf import settings
from . import views


urlpatterns = [
    path('login', views.login, name="login"),
    path('sign_up', views.signUp, name="sign_up"),
    path('homepage', views.search, name="home_page"),
    path('search', views.searchResult, name="search_result")
=======


urlpatterns = [
    path('login', home.login, name="login"),
    path('sign_up', home.signUp, name="sign_up"),
    path('homepage', home.homeView, name="home_page")
>>>>>>> 8ad19a3b2a333c6c8ca948541eddfda28db26f50
]