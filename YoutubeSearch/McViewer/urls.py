from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('login', views.login, name="login"),
    path('sign_up', views.signUp, name="sign_up"),
    path('homepage', views.search, name="home_page")
]