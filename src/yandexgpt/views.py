import asyncio

import httpx
from django.conf import settings

from yandexgpt.constants import ERROR_MESSAGE, GPT_SYSTEM_ROLE, GPT_URL


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

    async def generate_text(self, prompt):
        """Отправляет асинхронный запрос к YandexGPT."""
        async with httpx.AsyncClient() as client:
            payload = {
                "modelUri": f"gpt://{self.folder_id}/yandexgpt-pro",
                "completionOptions": {
                    "stream": False,
                    "temperature": 0.6,
                    "maxTokens": 2000,
                },
                "messages": [
                    {"role": "system", "text": GPT_SYSTEM_ROLE},
                    {"role": "user", "text": prompt},
                ],
            }
            response = await client.post(
                self.base_url,
                headers=self.headers,
                json=payload,
            )
            if response.status_code == 200:
                operation_id = response.json()['id']
                return await self.wait_for_completion(client, operation_id)
            else:
                return ERROR_MESSAGE

    async def wait_for_completion(self, client, operation_id):
        """Ожидает завершения операции и возвращает результат."""
        while True:
            response = await client.get(
                f'https://llm.api.cloud.yandex.net/operations/{operation_id}',
                headers=self.headers,
            )
            if response.status_code == 200:
                operation_response = response.json()
                if operation_response.get('done', False):
                    return operation_response['response']['alternatives'][0][
                        'message']['text']
                else:
                    await asyncio.sleep(0.5)
            else:
                return ERROR_MESSAGE
