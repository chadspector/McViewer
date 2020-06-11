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
    path('getRelatedSearch/<str:search>', views.getRelatedSearch, name="getRelatedSearch"),
    path('edit_profile/<str:username>',views.editProfile, name="edit_profile"),
    path('network/<str:username>', views.network, name = "network"),
    path('network/<str:username>/<str:title>', views.privateNetwork, name = "private_network")
]