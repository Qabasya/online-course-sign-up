# Работа с базой данных
import aiosqlite

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
    """
    Создаёт таблицу clients, если она ещё не существует
    """
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


async def add_client(
        course: str,
        school: str,
        name: str,
        phone: str | None,
        user_id: int,
        username: str | None = None,
) -> None:
    """
    Добавление новой записи в таблицу clients

    Параметры:
        course   : выбранное направление
        school   : класс и школа
        name     : имя
        phone    : телефон (может быть None)
        user_id  : telegram id пользователя
        username : @username без собаки (или None)
    """
    if username is None:
        username = 'нет username'

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT INTO clients 
            (course, school, name, phone, user_id, username)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (course, school, name, phone, user_id, username))

        await db.commit()
