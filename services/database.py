# Работа с базой данных
import  sqlite3

DB_NAME = 'sign_up_bot.db'
DB_PATH = f'db/{DB_NAME}'
#== Структура таблицы   ==#
# id -> идентификатор записи
# course -> название курса
# class_school -> данные о класе и школе
# name -> имя
# phone -> телефон
# user_id -> id пользователя
# username -> имя пользователя
# date -> дата добавления записи
#==                      ==#

def init_db() -> None:
    """
    Создание таблицы clients в базе DB_NAME
    :return: None
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course TEXT NOT NULL,
            school TEXT NOT NULL,
            name TEXT NOT NULL,
            phone TEXT,
            user_id INTEGER NOT NULL,
            username TEXT DEFAULT 'нет username',
            reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def add_client(course:str, school:str, name:str, phone:str, user_id:int, username=None )->None:
    """
    Добавление новой записи в таблицу clients
    :param course: выбранное направление
    :param school: класс и школа
    :param name: имя
    :param phone: телефон
    :param user_id: id пользователя
    :param username: username, при наличии
    :return: None
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        if username is None:
            username = 'нет username'
        cursor.execute('''
                    INSERT INTO clients (course, school, name, phone, user_id, username)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (course, school, name, phone, user_id, username))
        conn.commit()



