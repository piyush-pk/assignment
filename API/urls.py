from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('register', register, name = 'register'),
    path('delete', delete, name = 'delete'),
    path('profile', profile, name = 'profile'),
    path('update/<int:id>', update, name = 'update'),
]
