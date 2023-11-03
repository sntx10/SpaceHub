import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from chat.models import ChatRoomParticipant

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """При подключении клиента к вебсокету"""

        # Извлекаем имя комнаты из URL-маршрута
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # Формируем уникальное имя группы на основе имени комнаты
        self.room_group_name = f'chat_{self.room_name}'

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Отправляем сообщение о том, что пользователь присоединился к чату
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_entered',
                'message': f'{self.scope["user"].username} зашел в чат'
            }
        )

        # Принимаем вебсокет-соединение
        await self.accept()

    async def disconnect(self, close_code):
        """При отключении клиента от вебсокета"""

        # Покидаем группу
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Отправляем сообщение о том, что пользователь покинул чат
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_left',
                'message': f'{self.scope["user"].username} вышел из чата'
            }
        )

    async def receive(self, text_data):
        """При получении сообщения от клиента"""

        # Разбор полученных данных
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        action = text_data_json.get('action')

        # Если действие - это блокировка пользователя
        if action == "ban_user":
            # Проверяем, является ли текущий пользователь админом
            if not await self._is_admin():
                await self.send(text_data=json.dumps({
                    "error": "У вас нет прав блокировать пользователей."
                }))
                return

            # Блокируем указанного пользователя
            user_to_ban = User.objects.get(username=text_data_json["username"])
            participant = ChatRoomParticipant.objects.get(chatroom=self.room_group_name, user=user_to_ban)
            participant.is_banned = True
            participant.save()

            # Отправляем сообщение о блокировке пользователя
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_banned',
                    'message': f'{user_to_ban.username} был заблокирован {self.scope["user"].username}'
                }
            )

        else:  # Отправка обычного сообщения
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_message',
                    'message': f'{self.scope["user"].username}: {message}'
                }
            )

    async def chat_message(self, event):
        """Отправка сообщения всем участникам чата"""

        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def user_entered(self, event):
        """Обработка входа пользователя в чат"""
        await self.send(text_data=json.dumps(event))

    async def user_left(self, event):
        """Обработка выхода пользователя из чата"""
        await self.send(text_data=json.dumps(event))

    async def user_message(self, event):
        """Обработка отправки сообщения от одного пользователя другому"""
        await self.send(text_data=json.dumps(event))
