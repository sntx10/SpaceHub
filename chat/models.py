from django.db import models
from django.conf import settings


class ChatRoomManager(models.Manager):
    def create_or_get_private_chat(self, user1, user2):
        room = self.filter(participants__in=[user1, user2])
        if room.count() == 1:
            return room.first()
        room = self.create()
        room.participants.add(user1, user2)
        return room


class ChatRoom(models.Model):
    title = models.CharField(max_length=100)
    chat_image = models.ImageField(upload_to='media/chat_image/')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chatrooms')
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chatrooms_created', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_chatrooms', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = ChatRoomManager()

    def add_participant(self, user):
        self.participants.add(user)

    def remove_participant(self, user):
        if user != self.created_by:
            self.participants.remove(user)


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp}"


class ChatRoomParticipant(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)

