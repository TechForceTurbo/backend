import os
import threading

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv

from chat.models import ChatSession
from telegarm_bot.YandexGPT import response_logic

load_dotenv()

router = Router()

TOKEN = os.getenv('TOKEN')


@router.message(Command(commands=["start"]))
async def start_command_handler(message: Message):
    """Обработчик команды start."""

    user_id = message.chat.id
    ChatSession.objects.get_or_create(session_id=user_id, source='TG')
    await message.answer('Здравствуйте, консультант магазина'
                         ' Винк готов ответить на ваши вопросы.')


@router.message()
async def message_handler(message: types.Message):
    """Обработчик любого текстового сообщения."""

    user_id = message.chat.id
    session = ChatSession.objects.get_or_create(session_id=user_id,
                                                source='TG')[0]
    thread = threading.Thread(target=response_logic, args=(message.text,
                                                           session,
                                                           message.from_user.id,
                                                           message.message_id,
                                                           message.from_user.username))
    thread.start()
