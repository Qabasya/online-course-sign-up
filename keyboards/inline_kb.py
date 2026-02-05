from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON_BUTTONS, LEXICON_MENU


def get_courses_keyboard() -> InlineKeyboardMarkup:
    """
    Клавиатура выбора курса.
    """

    # Создаём builder
    builder = InlineKeyboardBuilder()

    # Список курсов (можно загружать из БД)
    courses = [
        ("📘 ОГЭ", "course_oge"),
        ("📗 ЕГЭ", "course_ege"),
        ("🐍 Python", "course_python"),
    ]

    # Добавляем кнопки в цикле
    for text, callback in courses:
        builder.button(text=text, callback_data=callback)

    # Настраиваем расположение: 1 кнопка в ряду
    builder.adjust(1)

    # Возвращаем готовую клавиатуру
    return builder.as_markup()


def get_course_detail_keyboard(course_id: str) -> InlineKeyboardMarkup:
    """
    Клавиатура для страницы курса
    """
    builder = InlineKeyboardBuilder()

    # Добавляем кнопки по одной в ряд (каждая в новом ряду)
    builder.button(
        text=LEXICON_BUTTONS['signup'],
        callback_data=f"signup_{course_id}"
    )
    builder.button(
        text=LEXICON_BUTTONS['back_to_courses'],
        callback_data="back_to_courses"
    )

    # Выстраиваем кнопки вертикально (1 кнопка в ряду)
    builder.adjust(1)

    return builder.as_markup()