from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter

from keyboards.reply_kb import get_main_menu_keyboard
from keyboards.inline_kb import get_courses_keyboard, get_course_detail_keyboard
from lexicon.lexicon import (
    LEXICON_MENU,
    LEXICON_COURSES,
    LEXICON_ABOUT,
    LEXICON_PROJECTS
)

# Создаём роутер
router = Router(name='menu_router')


# ===== REPLY КНОПКИ МЕНЮ =====

# Наши курсы
@router.message(F.text == LEXICON_MENU['courses'], StateFilter(default_state))
async def show_courses(message: Message):
    """
    Обработчик кнопки "Наши курсы".

    StateFilter(default_state) - только если нет активного состояния
    """

    # Отправляем список курсов с Inline клавиатурой
    await message.answer(
        text=LEXICON_COURSES['select'],
        reply_markup=get_courses_keyboard()
    )


# О нас
@router.message(F.text == LEXICON_MENU['about'], StateFilter(default_state))
async def show_about(message: Message):
    """
    Обработчик кнопки "О нас".
    """
    # Информация о школе (без inline кнопок, просто текст)
    await message.answer(
        text=LEXICON_ABOUT,
        reply_markup=get_main_menu_keyboard()
    )


# Проекты
@router.message(F.text == LEXICON_MENU['projects'], StateFilter(default_state))
async def show_projects(message: Message):
    """
    Обработчик кнопки "Примеры проектов".
    """
    await message.answer(
        text=LEXICON_PROJECTS,
        reply_markup=get_main_menu_keyboard()
    )


# ===== INLINE КНОПКИ ВЫБОРА КУРСА =====
@router.callback_query(F.data.startswith("course_"))
async def show_course_detail(callback: CallbackQuery):
    """
    Обработчик inline кнопок выбора курса.
    """
    course_id = callback.data.split("_")[1]

    # Получаем описание курса
    course_text = LEXICON_COURSES.get(course_id)

    # Редактируем сообщение (заменяем текст и клавиатуру)
    await callback.message.edit_text(
        text=course_text,
        reply_markup=get_course_detail_keyboard(course_id)
    )

    await callback.answer()


@router.callback_query(F.data == "back_to_courses")
async def back_to_courses(callback: CallbackQuery):
    """
    Кнопка "Назад к списку курсов".
    """
    await callback.message.edit_text(
        text=LEXICON_COURSES['select'],
        reply_markup=get_courses_keyboard()
    )

    await callback.answer()

