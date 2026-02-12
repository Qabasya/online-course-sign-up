import asyncio
import os
import logging.config
import pathlib

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


def prepare_directories(dirs: list[str]):
    """Создает необходимые папки и проверяет права доступа."""
    for dir_name in dirs:
        path = pathlib.Path(__file__).parent / dir_name
        try:
            path.mkdir(parents=True, exist_ok=True)
            # Тест на запись
            test_file = path / ".write_test"
            test_file.touch()
            test_file.unlink()
        except Exception as e:
            print(f"Критическая ошибка: нет прав на папку {dir_name}. Ошибка: {e}")

# Список папок, которые нужны боту для работы
REQUIRED_DIRS = ["logs", "db"]
prepare_directories(REQUIRED_DIRS)

# Теперь загружаем логи, когда папка 'logs' точно есть
with open('logging_config.yaml', 'rt') as f:
    config = yaml.safe_load(f.read())

logging.config.dictConfig(config)
logger = logging.getLogger(__name__)
logger.info('Бот запускается...')

#Debug
logger.warning('Тест warning')
logger.error('Тест errors')
logger.critical('Тест critical')


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
