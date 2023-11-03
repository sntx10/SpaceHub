from django.contrib import admin

from feedback import models

# Register your models here.

admin.site.register(models.Comment)
admin.site.register(models.Like)
admin.site.register(models.Favorite)