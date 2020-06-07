from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    # path('login', views.login, name="login"),
    path('sign_up', views.signUp, name="sign_up"),
    path('homepage/<str:username>', views.index, name="home_page"),
    path('search/<str:search>', views.searchResult, name="search_result"),
    path('getRelatedSearch/<str:search>', views.getRelatedSearch, name="getRelatedSearch"),
    path('edit_profile/<str:username>',views.editProfile, name="edit_profile")
]