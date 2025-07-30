'''
The set of available commands in the bot menu
'''
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

COMMANDS = [
    {'command': 'start', 'description': 'The start of work'},
    {'command': 'help', 'description': 'I need a help'},
    {'command': 'weather', 'description': 'Geat a weather'},
]

async def set_commands(bot: Bot):
    """
    Sets a list of commands for the bot.
    Args:
        bot (Bot): Instance of the bot.
    """
    # Create a list of BotCommand objects from the COMMANDS constant
    commands = [BotCommand(command=cmd['command'], description=cmd['description']) for cmd in COMMANDS]
    # Set up commands for the bot
    await bot.set_my_commands(commands, BotCommandScopeDefault())