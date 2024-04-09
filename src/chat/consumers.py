import json
import uuid
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

from chat.models import ChatMessage, ChatSession
from yandexgpt.constants import ROLE_ASSISTANT, ROLE_USER
from yandexgpt.views import YandexGPTClient

gpt_client = YandexGPTClient()


class ChatConsumer(AsyncWebsocketConsumer):
    """
    Асинхронный WebSocket потребитель для обработки чат-сессий.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = []
        self.session_id = None
        self.session = None

    async def connect(self):
        """
        Обрабатывает подключение к WebSocket.
        """
        query_string = self.scope['query_string'].decode()
        params = parse_qs(query_string)
        session_id = params.get('session_id', [str(uuid.uuid4())])[0]
        self.session_id = session_id
        self.session = await self.get_or_create_session()
        await self.accept()
        await self.send(text_data=json.dumps({'session_id': self.session_id}))

    async def disconnect(self, close_code):
        """
        Обрабатывает отключение от WebSocket.
        """
        pass

    async def save_context(self, message, role=ROLE_USER):
        """
        Сохраняет сообщение в контекст диалога.
        """
        self.context.append({"role": role, "text": message})
        if len(self.context) > settings.GPT_MAX_CONTEXT_LENGTH:
            self.context.pop(0)

    async def receive(self, text_data):
        """
        Обрабатывает получение текстового сообщения от клиента, обновляет
        контекст диалога, генерирует ответ на основе текущего контекста
        и отправляет его обратно клиенту. А также сохраняет сообщения в базу
        данных.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.save_context(message)
        await self.save_message(message)

        bot_response = await gpt_client.generate_text(self.context)

        await self.save_context(bot_response, ROLE_ASSISTANT)
        await self.save_message(bot_response, is_user_message=False)
        await self.send(text_data=json.dumps({'message': bot_response}))

    @database_sync_to_async
    def get_or_create_session(self, source='WEB'):
        """
        Получает или создает сессию чата в базе данных.
        """
        session, _ = ChatSession.objects.get_or_create(
            session_id=self.session_id, source=source
        )
        return session

    @database_sync_to_async
    def save_message(self, message, is_user_message=True):
        """
        Сохраняет сообщение чата в базу данных.
        """
        return ChatMessage.objects.create(
            session=self.session,
            message=message,
            is_user_message=is_user_message
        )
