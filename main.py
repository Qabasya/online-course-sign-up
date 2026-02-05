import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import load_config
from handlers.start import router as start_router


async def main():
    config = load_config()

    # ===== СОЗДАНИЕ БОТА =====
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML  # HTML разметка по умолчанию
        )
    )

    # ===== СОЗДАНИЕ ДИСПЕТЧЕРА =====
    dp = Dispatcher()

    # ===== ПОДКЛЮЧЕНИЕ РОУТЕРОВ =====
    dp.include_router(start_router)  # 1. Команды /start, /help

    # ===== ЗАПУСК POLLING =====
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Запускаем асинхронную функцию
    asyncio.run(main())