import asyncio
import json
import uuid

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        session_id = self.scope['cookies'].get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())

        self.session_id = session_id
        await self.send(text_data=json.dumps({'session_id': self.session_id}))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await asyncio.sleep(2)
        await self.send(text_data=json.dumps({
            'message': message,
            'sessin_id': self.session_id
        }))
