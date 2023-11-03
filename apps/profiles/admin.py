from django.contrib import admin

# Register your models here.

from apps.profiles import models
from apps.profiles.models import UserProfile

admin.site.register(UserProfile)
