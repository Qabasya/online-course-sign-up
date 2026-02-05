from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)

from lexicon.lexicon import LEXICON_MENU, LEXICON_BUTTONS


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


def get_contact_keyboard() -> ReplyKeyboardMarkup:
    """
    Клавиатура для запроса контакта пользователя.

    request_contact=True - при нажатии отправляет номер телефона.
    Работает только если пользователь привязал номер к Telegram.
    """

    # Кнопка отправки контакта (специальная)
    button_contact = KeyboardButton(
        text=LEXICON_BUTTONS['send_contact'],
        request_contact=True
    )

    # Кнопка отмены (обычная)
    button_cancel = KeyboardButton(text=LEXICON_BUTTONS['cancel'])

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [button_contact], [button_cancel]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return keyboard


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """
    Клавиатура только с кнопкой отмены.
    Используется во время заполнения формы.
    """

    button_cancel = KeyboardButton(text=LEXICON_BUTTONS['cancel'])

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_cancel]],
        resize_keyboard=True
    )

    return keyboard

