from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import GolfUser

admin.site.register(GolfUser, UserAdmin)
