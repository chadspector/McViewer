from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    path('login', views.loginprofile, name="login"),
    path('sign_up', views.signUp, name="sign_up"),
    path('homepage/<str:username>', views.index, name="home_page"),
    path('search', views.searchResult, name="search_result"),
<<<<<<< HEAD
=======
    path('getRelatedSearch/<str:search>', views.getRelatedSearch, name="getRelatedSearch"),
>>>>>>> e23a8420a8106f6e13960864a1833fb0825e092b
    path('edit_profile/<str:username>',views.editProfile, name="edit_profile")
]