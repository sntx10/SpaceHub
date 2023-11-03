from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import consumers
from .views import ChatRoomViewSet, MessageViewSet, index

router = DefaultRouter()
router.register(r'chatrooms', ChatRoomViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('ws/chat/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    path('', include(router.urls)),
]
