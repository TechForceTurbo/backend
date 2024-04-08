import pytest

from unittest.mock import AsyncMock
from .handlers import start_command_handler


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_start_command_handler():
    message = AsyncMock()
    await start_command_handler(message)
    message.answer.assert_called_with('Здравствуйте, консультант магазина Винк готов ответить на ваши вопросы.')
