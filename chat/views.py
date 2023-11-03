from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


User = get_user_model()


class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        chatroom = serializer.save(created_by=self.request.user, admin=self.request.user)
        chatroom.participants.add(self.request.user)

    @action(detail=False, methods=['post'], url_path='private_chat/(?P<user2_id>\d+)')
    def create_or_get_private_chat(self, request, user2_id=None):
        user1 = request.user
        user2 = get_object_or_404(User, id=user2_id)

        chat_room = ChatRoom.objects.create_or_get_private_chat(user1, user2)

        return Response({"chat_room_id": chat_room.id, "message": "Private chat created or retrieved successfully"},
                        status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)


def index(request):
    return render(request, 'chat/index.html')


