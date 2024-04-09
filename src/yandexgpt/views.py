import asyncio
from http import HTTPStatus

import httpx
from django.conf import settings
from httpx import AsyncClient

from yandexgpt.constants import (
    ERROR_MESSAGE,
    GPT_SYSTEM_ROLE,
    GPT_URL,
    ROLE_SYSTEM,
)


class YandexGPTClient:
    """
    Клиент для взаимодействия с YandexGPT API.

    Позволяет отправлять асинхронные запросы к YandexGPT для генерации текста и
    отслеживать их выполнение.
    """
    def __init__(self):
        self.api_key = settings.YANDEX_GPT_API_KEY
        self.folder_id = settings.YANDEX_FOLDER_ID
        self.base_url = GPT_URL
        self.headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json",
        }

    async def generate_text(self, context: list) -> str:
        """Отправляет асинхронный запрос к YandexGPT."""
        messages = [
            {"role": ROLE_SYSTEM, "text": GPT_SYSTEM_ROLE}
        ]
        messages.extend(context)
        async with httpx.AsyncClient() as client:
            payload = {
                "modelUri": f"gpt://{self.folder_id}/yandexgpt-pro",
                "completionOptions": {
                    "stream": False,
                    "temperature": 0.6,
                    "maxTokens": 2000,
                },
                "messages": messages,
            }
            response = await client.post(
                self.base_url,
                headers=self.headers,
                json=payload,
            )
            if response.status_code == HTTPStatus.OK:
                operation_id = response.json()['id']
                return await self._wait_for_completion(client, operation_id)
            else:
                print(response.json())
                return ERROR_MESSAGE

    async def _wait_for_completion(self, client: AsyncClient,
                                   operation_id: str) -> str:
        """Ожидает завершения операции и возвращает результат."""
        while True:
            response = await client.get(
                f'https://llm.api.cloud.yandex.net/operations/{operation_id}',
                headers=self.headers,
            )
            if response.status_code == HTTPStatus.OK:
                operation_response = response.json()
                if operation_response.get('done', False):
                    return operation_response['response']['alternatives'][0][
                        'message']['text']
                else:
                    await asyncio.sleep(0.5)
            else:
                return ERROR_MESSAGE
