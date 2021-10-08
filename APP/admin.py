from django.contrib import admin
from .models import *

class adminUser(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_superuser', 'is_superuser']

admin.site.register(User, adminUser)
