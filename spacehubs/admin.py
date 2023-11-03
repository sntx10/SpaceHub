from django.contrib import admin

from spacehubs import models

# Register your models here.

admin.site.register(models.Category)
admin.site.register(models.News)
admin.site.register(models.Blog)
admin.site.register(models.PodCast)
admin.site.register(models.Post)
admin.site.register(models.Project)
admin.site.register(models.ProjectView)
admin.site.register(models.BlogView)
admin.site.register(models.PostView)
admin.site.register(models.PodCastView)
admin.site.register(models.NewsView)
