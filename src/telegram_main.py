import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from telegarm_bot.handlers import router

load_dotenv()

TOKEN = os.getenv('TOKEN')


async def main_2():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
