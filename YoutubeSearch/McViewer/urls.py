from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
<<<<<<< HEAD
from django.conf import settings
from . import views


urlpatterns = [
    path('login', views.login, name="login"),
    path('sign_up', views.signUp, name="sign_up"),
<<<<<<< HEAD
    path('homepage', views.index, name="home_page")
=======
    path('homepage', views.search, name="home_page"),
    path('search', views.searchResult, name="search_result")
>>>>>>> f1b35a7494e30203f2061126429b539255fb2a13
]