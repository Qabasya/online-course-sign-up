from aiogram import types
from aiogram.exceptions import TelegramBadRequest


async def send_message(
        target: types.Message | types.CallbackQuery,
        text: str,
        reply_markup=None
):
    """
    Безопасная отправка сообщения.
    Сначала пытается отредактировать, если не получается — отправляет новое.
    """

    # Определяем, с чем работаем
    if isinstance(target, types.CallbackQuery):
        message = target.message
    else:
        message = target

    # Если есть reply-клавиатура — редактировать нельзя
    is_reply_keyboard = isinstance(reply_markup, types.ReplyKeyboardMarkup)

    try:
        if is_reply_keyboard:
            # При reply-клавиатуре редактировать нельзя → сразу отправляем новое
            await message.answer(
                text=text,
                reply_markup=reply_markup
            )
        else:
            # Inline или None — можно попробовать отредактировать
            await message.edit_text(
                text=text,
                reply_markup=reply_markup
            )
    except TelegramBadRequest as e:
        # Если редактирование всё равно упало (например, "message is not modified")
        # или просто сообщение слишком старое — отправляем новое
        await message.answer(
            text=text,
            reply_markup=reply_markup
        )