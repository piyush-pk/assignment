from django.db import models
from django.contrib.auth.models import AbstractUser
from .user_manager import UserManager
# from django.contrib.auth import get_user_model

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=250)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

# User = get_user_model()