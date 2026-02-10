import asyncio
import logging.config

import yaml
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramNetworkError
from aiogram.fsm.storage.memory import MemoryStorage

from config import load_config
from handlers.menu import router as menu_router
from handlers.signup import router as signup_router
from handlers.start import router as start_router
from keyboards.bot_commands import set_main_menu
from services.database import init_db

with open('logging_config.yaml', 'rt') as f:
    config = yaml.safe_load(f.read())

logging.config.dictConfig(config)

logger = logging.getLogger(__name__)
logger.info('Бот запускается...')


async def main():
    logger.info("Инициализация базы данных...")
    await init_db()
    logger.info("База данных готова")

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
    try:
        await set_main_menu(bot)
    except TelegramNetworkError as e:
        logger.warning(f"Ошибка сети в установке меню: {e}")
        logger.debug("Тип ошибки: %s", type(e))
        return
    except Exception as e:
        logger.critical(f"Не удалось установить меню: {e}")

    # ===== ЗАПУСК POLLING =====
    try:
        await dp.start_polling(bot)
    except TelegramNetworkError as e:
        logger.warning(f"Ошибка сети в pulling: {e}")
    except Exception as e:
        logger.critical(f"Критическая ошибка polling: {e}")


if __name__ == "__main__":
    # Запускаем асинхронную функцию
    try:
        asyncio.run(main())
    except TelegramNetworkError as e:
        logger.error(f"Ошибка сети в main: {e}")
