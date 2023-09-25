from aiogram import Bot
from aiogram.types import BotCommand,BotCommandScopeDefault


async def set_default_commands(bot: Bot):
    commands = ([
        BotCommand(command="start",
                   description= "Запустить бота"),
        BotCommand(command="info",
                   description= "Информация о Нас"),
        BotCommand(command="card",
                   description= "Карта лояльности"),
        BotCommand(command='check_in',
                   description='Отметить посещение')
    ])

    await bot.set_my_commands(commands,
                              BotCommandScopeDefault())

