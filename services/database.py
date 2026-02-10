# Работа с базой данных
import aiosqlite
import logging

# Получаем логгер для базы данных (он будет использовать настройки из секции database в YAML)
logger = logging.getLogger('database')

DB_NAME = 'sign_up_bot.db'
DB_PATH = f'db/{DB_NAME}'


# == Структура таблицы   ==#
# id -> идентификатор записи
# course -> название курса
# class_school -> данные о класе и школе
# name -> имя
# phone -> телефон
# user_id -> id пользователя
# username -> имя пользователя
# date -> дата добавления записи
# ==                      ==#

async def init_db() -> None:
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id       INTEGER PRIMARY KEY AUTOINCREMENT,
                    course   TEXT    NOT NULL,
                    school   TEXT    NOT NULL,
                    name     TEXT    NOT NULL,
                    phone    TEXT,
                    user_id  INTEGER NOT NULL,
                    username TEXT    DEFAULT 'нет username',
                    reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            await db.commit()
            logger.info('База данных создана')
    except aiosqlite.Error as e:
        # Это уровень CRITICAL, так как без БД бот бесполезен
        logger.critical(f"Критическая ошибка при инициализации БД: {e}", exc_info=True)
        raise


async def add_client(
        course: str,
        school: str,
        name: str,
        phone: str | None,
        user_id: int,
        username: str | None = None,
) -> None:
    if username is None:
        username = 'нет username'

    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute('''
                INSERT INTO clients 
                (course, school, name, phone, user_id, username)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (course, school, name, phone, user_id, username))
            await db.commit()
            logger.info(f"Добавлен новый клиент: {user_id}")

    except aiosqlite.Error as e:
        # Это уровень ERROR, так как конкретная запись не добавилась
        logger.error(f"Ошибка при добавлении клиента {user_id}: {e}", exc_info=True)
    except Exception as e:
        # На случай непредвиденных ошибок (проблемы с типами данных и т.д.)
        logger.error(f"Неизвестная ошибка: {e}", exc_info=True)
