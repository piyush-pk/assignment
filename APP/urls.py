from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home, name = 'home'),
    # path('logout', logout, name = 'logout'),
    path('register', register, name = 'register'),
    path('profile', profile, name = 'profile'),
    path('update', update, name = 'update'),
    path('logout', logout_view, name = 'logout_view'),
    path('delete', delete, name = 'delete'),
]
