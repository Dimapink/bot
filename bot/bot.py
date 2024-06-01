from utils.config import settings
from aiogram import Bot, Dispatcher
from bot.commands import router

bot = Bot(token=settings.API_KEY)
dispatcher = Dispatcher()


async def start():
    """Асинхронный метод для обработки запросов с серверов telegram, если ответа нет, ожидаем входящий запрос"""
    dispatcher.include_router(router)
    await dispatcher.start_polling(bot)

