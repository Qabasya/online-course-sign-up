from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)

from lexicon.lexicon import LEXICON_MENU


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """
    Создаёт главное меню бота.

    Возвращает клавиатуру с кнопками:
    - Наши курсы
    - О нас
    - Примеры проектов

    resize_keyboard=True - уменьшает размер кнопок
    one_time_keyboard=False - клавиатура НЕ скрывается после нажатия
    """

    # Создаём кнопки
    button_courses = KeyboardButton(text=LEXICON_MENU['courses'])
    button_about = KeyboardButton(text=LEXICON_MENU['about'])
    button_projects = KeyboardButton(text=LEXICON_MENU['projects'])

    # Собираем клавиатуру
    # keyboard - список списков (строки кнопок)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [button_courses],  # Первая строка - 1 кнопка
            [button_about, button_projects]  # Вторая строка - 2 кнопки
        ],
        resize_keyboard=True,  # Уменьшаем размер кнопок
        one_time_keyboard=False,  # Не скрываем после нажатия
        input_field_placeholder="Выберите пункт меню..."  # Подсказка в поле ввода
    )

    return keyboard