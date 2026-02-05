from aiogram.types import BotCommand


async def set_main_menu(bot):
    commands = [
        BotCommand(command='/start', description='Начало работы'),
        BotCommand(command='/help', description='Помощь'),
        BotCommand(command='/cancel', description='Отмена'),
    ]

    await bot.set_my_commands(commands)
