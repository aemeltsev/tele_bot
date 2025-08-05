import asyncio
import logging
import os
from dotenv import load_dotenv
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command

from core.utils.commands import set_commands # Import to create menu button
# Import handlers for start, help and weather commands, for dispatcher processing
from core.handlers.basic import cmd_start, cmd_help, cmd_weather, cmd_login, cmd_signup

logger = logging.getLogger(__name__)

load_dotenv()

async def start_bot(bot: Bot):
    """Notify admin that the bot is running."""
    bot_info = await bot.me()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    admin_id = os.getenv('ADMIN_ID')
    message_text = (
        f'Bot {bot_info.first_name} is running!\n'
        f'Admin ID: {admin_id}\n'
        f'Current Time: {current_time}\n'
        f'Bot ID: {bot_info.id}\n'
        f'Bot Username: @{bot_info.username}'
    )
    logger.info(f'{message_text}')
    #await bot.send_message(settings.bots.admin_id, text='Bot is running!')

async def stop_bot(bot: Bot):
    """Notify admin that the bot is running."""
    bot_info = await bot.me()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    admin_id = os.getenv('ADMIN_ID')
    message_text = (
        f'Bot {bot_info.first_name} is stopping!\n'
        f'Admin ID: {admin_id}\n'
        f'Current Time: {current_time}\n'
        f'Bot ID: {bot_info.id}\n'
        f'Bot Username: @{bot_info.username}\n'
        "#####################################"
    )
    logger.info(f'{message_text}')
    #await bot.send_message(settings.bots.admin_id, text='Bot is stopping!')

def configure_logging():
    """Configure logging settings."""
    logging.basicConfig(
        filename='files/logs/log.txt',
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )

def register_handlers(dp: Dispatcher):
    """
    Register all handlers for the dispatcher.
    Let's register a handler, the event we register for is message.
    Let's call the registry method, which will launch the process_start_command function.
    """
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(cmd_start, Command('start'))
    dp.message.register(cmd_help, Command('help'))
    dp.message.register(cmd_weather, Command('weather'))
    dp.message.register(cmd_login, Command('login'))
    dp.message.register(cmd_signup, Command('signup'))

async def main() -> None:
    """Main function to start the bot."""
    configure_logging()
    bot_token = os.getenv('TOKEN')
    # Create an object of the bot class
    bot = Bot(token=bot_token)
    # Create an object of the dispatcher class it is receiving updates
    dp = Dispatcher()

    register_handlers(dp)

    try:
        # 
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"An error occurred while polling: {e}")
    finally:
        # 
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())