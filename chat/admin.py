from django.contrib import admin
from . import models

admin.site.register(models.ChatRoom)
admin.site.register(models.Message)
admin.site.register(models.ChatRoomParticipant)