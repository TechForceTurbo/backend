import asyncio
import json
import uuid
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import ChatMessage, ChatSession
from yandexgpt.views import YandexGPTClient

gpt_client = YandexGPTClient()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope['query_string'].decode()
        params = parse_qs(query_string)
        session_id = params.get('session_id', [str(uuid.uuid4())])[0]
        self.session_id = session_id
        self.session = await self.get_or_create_session()
        await self.accept()
        await self.send(text_data=json.dumps({'session_id': self.session_id}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Сохраняем сообщение пользователя в базу данных
        await self.save_message(message)

        # Отправляем сообщение в YandexGPT и ждем ответа
        bot_response = await gpt_client.generate_text(message)

        # Сохраняем ответ от GPT в базу данных как сообщение от системы
        await self.save_message(bot_response, is_user_message=False)

        # Отправляем ответ обратно клиенту через WebSocket
        await self.send(text_data=json.dumps({'message': bot_response}))

    @database_sync_to_async
    def get_or_create_session(self, source='WEB'):
        session, _ = ChatSession.objects.get_or_create(
            session_id=self.session_id, source=source
        )
        return session

    @database_sync_to_async
    def save_message(self, message, is_user_message=True):
        return ChatMessage.objects.create(
            session=self.session,
            message=message,
            is_user_message=is_user_message
        )
