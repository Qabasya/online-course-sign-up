from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message

from keyboards.reply_kb import get_main_menu_keyboard
from lexicon.lexicon import LEXICON_START, LEXICON_HELP
from utils.messages import send_message

import logging

logger = logging.getLogger(__name__)

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
    user = message.from_user
    logger.info(f"Пользователь {user.id} (@{user.username}) нажал /start")

    await send_message(message, text=LEXICON_START, reply_markup=get_main_menu_keyboard())



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
    user = message.from_user
    logger.debug(f"Пользователь {user.id} (@{user.username}) нажал /start в состоянии {state}")
    await state.clear()
    await send_message(message, text=LEXICON_START, reply_markup=get_main_menu_keyboard())



@router.message(Command("help"))
async def cmd_help(message: Message):
    """
    Обработчик команды /help.
    """
    user = message.from_user
    logger.info(f"Пользователь {user.id} (@{user.username}) нажал /help")
    await send_message(message, text=LEXICON_HELP)