from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from keyboards.reply_kb import get_main_menu_keyboard
from lexicon.lexicon import LEXICON_START, LEXICON_HELP

# Создаём роутер для этого модуля
router = Router(name='start_router')


@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message):
    """
    Обработчик команды /start.

    CommandStart() - фильтр для команды /start
    StateFilter(default_state) - срабатывает только если пользователь
                                 НЕ находится в каком-либо состоянии FSM

    Это важно! Если пользователь заполняет форму и нажмёт /start,
    этот хендлер НЕ сработает (нужен другой хендлер для сброса)
    """

    await message.answer(
        text=LEXICON_START,
        reply_markup=get_main_menu_keyboard()
    )


@router.message(CommandStart())
async def cmd_start_reset(message: Message, state: FSMContext):
    """
    Обработчик /start когда пользователь В состоянии.

    Этот хендлер сработает если пользователь находится в процессе
    заполнения формы и хочет выйти через /start.

    Важно: хендлеры проверяются по порядку! Сначала проверится
    первый (с StateFilter(default_state)), и если не подошёл - этот.
    """

    # Сбрасываем состояние и очищаем данные
    await state.clear()

    await message.answer(
        text="🔄 Возвращаемся в главное меню...\n\n" + LEXICON_START, #todo разнести в разные сообщения
        reply_markup=get_main_menu_keyboard()
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """
    Обработчик команды /help.
    """
    await message.answer(text=LEXICON_HELP)