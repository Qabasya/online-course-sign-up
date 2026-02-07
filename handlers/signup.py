from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import load_config
from keyboards.reply_kb import (
    get_contact_keyboard,
    get_cancel_keyboard,
    get_main_menu_keyboard
)
from lexicon.lexicon import LEXICON_SIGNUP, LEXICON_ADMIN, COURSES_INFO, LEXICON_BUTTONS
from services.database import add_client
from states.signup import SignUpStates

# Загружаем конфиг и достаём ID администратора
config = load_config()
ADMIN_ID = config.bot.admin_id

# Создаём роутер
router = Router(name='signup_router')


# ===== НАЧАЛО РЕГИСТРАЦИИ =====

@router.callback_query(F.data.startswith("signup_"))
async def start_signup(callback: CallbackQuery, state: FSMContext):
    """
    Начало процесса записи на курс.
    Срабатывает при нажатии кнопки "Записаться на курс".
    """
    # Получаем ID курса
    course_id = callback.data.split("_")[1]
    course_name = COURSES_INFO.get(course_id)

    # Сохраняем выбранный курс в данные состояния
    # Эти данные будут доступны на всех следующих шагах
    await state.update_data(course_id=course_id, course_name=course_name)

    # Устанавливаем первое состояние - ожидание класса
    await state.set_state(SignUpStates.waiting_for_class)

    # Удаляем сообщение с inline кнопками
    await callback.message.delete()

    # Отправляем первый вопрос
    await callback.message.answer(
        text=LEXICON_SIGNUP['start'] + "\n" + LEXICON_SIGNUP['ask_class'],
        reply_markup=get_cancel_keyboard()  # Показываем кнопку отмены
    )

    await callback.answer()


# ===== ОТМЕНА РЕГИСТРАЦИИ =====
async def cancel_signup(message: Message, state: FSMContext):
    """
    Вспомогательная функция отмены регистрации.
    """

    # Получаем текущее состояние
    current_state = await state.get_state()

    if current_state is None:
        # Если и так нет состояния
        await message.answer(
            text="Нечего отменять 🤷‍♂️",
            reply_markup=get_main_menu_keyboard()
        )
        return

    # Очищаем состояние и данные
    await state.clear()

    await message.answer(
        text=LEXICON_SIGNUP['cancel'],
        reply_markup=get_main_menu_keyboard()
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """
    Обработчик команды /cancel.
    Отменяет регистрацию из любого состояния.
    """
    await cancel_signup(message, state)


# ===== ШАГ 1: КЛАСС И ШКОЛА =====

@router.message(StateFilter(SignUpStates.waiting_for_class), F.text)
async def process_class(message: Message, state: FSMContext):
    """
    Обработка ввода класса и школы.

    StateFilter(SignUpStates.waiting_for_class) - фильтр состояния!
    Этот хендлер сработает ТОЛЬКО если пользователь в состоянии waiting_for_class
    """

    # Проверяем на кнопку отмены
    if message.text == LEXICON_BUTTONS['cancel']:
        await cancel_signup(message, state)
        return

    # Простая валидация (можно добавить проверку формата)
    if len(message.text) < 3:
        await message.answer(
            text=LEXICON_SIGNUP['invalid_input'],
            parse_mode="HTML"
        )
        return

    # Сохраняем данные
    await state.update_data(class_school=message.text)

    # Переходим к следующему состоянию
    await state.set_state(SignUpStates.waiting_for_name)

    # Отправляем следующий вопрос
    await message.answer(
        text=LEXICON_SIGNUP['ask_name'],
        reply_markup=get_cancel_keyboard()
    )


# ===== ШАГ 2: ФИО =====

@router.message(StateFilter(SignUpStates.waiting_for_name), F.text)
async def process_name(message: Message, state: FSMContext):
    """
    Обработка ввода ФИО.
    """

    # Проверяем на кнопку отмены
    if message.text == LEXICON_BUTTONS['cancel']:
        await cancel_signup(message, state)
        return

    # Валидация ФИО (минимум 2 символа, есть пробелы)
    if len(message.text) < 2 or " " not in message.text:
        await message.answer(
            text="⚠️ Пожалуйста, введите полное ФИО (Фамилия Имя Отчество)"
        )
        return

    # Сохраняем ФИО
    await state.update_data(name=message.text)

    # Переходим к последнему шагу
    await state.set_state(SignUpStates.waiting_for_contact)

    # Запрашиваем контакт
    await message.answer(
        text=LEXICON_SIGNUP['ask_contact'],
        reply_markup=get_contact_keyboard()  # Клавиатура с кнопкой контакта
    )


# ===== ШАГ 3: КОНТАКТ =====

@router.message(StateFilter(SignUpStates.waiting_for_contact), F.contact)
async def process_contact(message: Message, state: FSMContext, bot: Bot):
    """
    Обработка полученного контакта.

    message.contact содержит:
    - phone_number: номер телефона
    - first_name: имя
    - last_name: фамилия (может быть None)
    - user_id: ID пользователя
    """

    # Получаем номер телефона из контакта
    phone = message.contact.phone_number
    user_id = message.from_user.id
    username = message.from_user.username

    # Сохраняем телефон
    await state.update_data(phone=phone)

    # Получаем ВСЕ собранные данные
    data = await state.get_data()

    # --- СОХРАНЕНИЕ В БАЗУ ДАННЫХ ---
    await add_client(
        course=data['course_name'],
        school=data['class_school'],
        name=data['name'],
        phone=phone,
        user_id=user_id,
        username=username
    )
    # --------------------------------

    # Формируем сообщение об успехе
    success_text = LEXICON_SIGNUP['success'].format(
        course=data['course_name'],
        class_school=data['class_school'],
        name=data['name'],
        phone=phone
    )

    # Отправляем подтверждение пользователю
    await message.answer(
        text=success_text,
        reply_markup=get_main_menu_keyboard()  # Возвращаем главное меню
    )

    # ===== ОТПРАВКА ЗАЯВКИ АДМИНУ =====
    admin_text = LEXICON_ADMIN.format(
        course=data['course_name'],
        class_school=data['class_school'],
        name=data['name'],
        phone=phone,
        user_id=message.from_user.id,
        username=message.from_user.username or "нет username",
        date=datetime.now().strftime("%d.%m.%Y %H:%M")
    )

    await bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_text,
    )

    # Очищаем состояние и данные
    await state.clear()


@router.message(StateFilter(SignUpStates.waiting_for_contact), F.text)
async def process_contact_text(message: Message, state: FSMContext):
    """
    Если пользователь ввёл текст вместо контакта.
    """

    # Проверяем на кнопку отмены
    if message.text == LEXICON_BUTTONS['cancel']:
        await cancel_signup(message, state)
        return

    await message.answer(
        text="⚠️ Пожалуйста, нажмите кнопку «📱 Отправить контакт» для отправки номера телефона.",
        reply_markup=get_contact_keyboard()
    )


# ===== ФИЛЬТР ЛЮБЫХ СООБЩЕНИЙ В СОСТОЯНИИ =====
@router.message(StateFilter(SignUpStates))
async def unknown_message_in_state(message: Message):
    """
    Ловит любые другие сообщения, когда пользователь в процессе регистрации.

    StateFilter(SignUpStates) - сработает для ЛЮБОГО состояния из группы SignUpStates

    Этот хендлер должен быть ПОСЛЕДНИМ, чтобы ловить только то,
    что не поймали другие хендлеры.
    """

    await message.answer(
        text="⚠️ Пожалуйста, следуйте инструкциям или используйте /cancel для отмены."
    )
