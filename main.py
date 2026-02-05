import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import load_config
from handlers.start import router as start_router
from handlers.menu import router as menu_router
from handlers.signup import router as signup_router
from keyboards.bot_commands import set_main_menu

async def main():
    config = load_config()

    # ===== СОЗДАНИЕ БОТА =====
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML  # HTML разметка по умолчанию
        )
    )

    # ===== ХРАНИЛИЩЕ FSM =====
    storage = MemoryStorage()

    # ===== СОЗДАНИЕ ДИСПЕТЧЕРА =====
    dp = Dispatcher(storage=storage)

    # ===== ПОДКЛЮЧЕНИЕ РОУТЕРОВ =====
    dp.include_router(start_router)  # 1. Команды /start, /help
    dp.include_router(signup_router)  # 2. FSM регистрации (важно раньше menu!)
    dp.include_router(menu_router)  # 3. Общие хендлеры меню

    # ===== КНОПКИ МЕНЮ С КОМАНДАМИ =====
    await set_main_menu(bot)

    # ===== ЗАПУСК POLLING =====
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Запускаем асинхронную функцию
    asyncio.run(main())