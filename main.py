import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import load_config
from handlers.menu import router as menu_router
from handlers.signup import router as signup_router
from handlers.start import router as start_router
from keyboards.bot_commands import set_main_menu
from services.database import init_db


async def main():
    config = load_config()

    # ===== СОЗДАНИЕ БОТА =====
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
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
    # Создаём базу
    init_db()
    # Запускаем асинхронную функцию
    asyncio.run(main())
