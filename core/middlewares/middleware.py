'''
Using Middlewares for Logging, Authentication, and Rate Limiting
'''

from aiogram import types, Dispatcher
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update
import logging
import time
from typing import Dict, Any


# Logging
logger = logging.getLogger(__name__)

# Mock database for user authentication
authenticated_users = {123456789, 987654321}

# Mock storage for rate limiting
user_request_times: Dict[int, float] = {}

class LoggingMiddleware(BaseMiddleware):
    """
    Middleware for logging updates.
    """
    async def on_process_update(self, update: Update, data: Dict[str, Any]):
        """
        Log the update before it is processed by handlers.

        Args:
            update (Update): The incoming update.
            data (Dict[str, Any]): The data dictionary.
        """
        if update.message:
            logger.info(f"Received message: {update.message.text}")
        elif update.callback_query:
            logger.info(f"Received callback query: {update.callback_query.data}")

class AuthMiddleware(BaseMiddleware):
    """
    Middleware for user authentication.
    """
    async def on_process_update(self, update: Update, data: Dict[str, Any]):
        """
        Check if the user is authenticated before processing the update.

        Args:
            update (Update): The incoming update.
            data (Dict[str, Any]): The data dictionary.
        """
        user_id = None
        if update.message:
            user_id = update.message.from_user.id
        elif update.callback_query:
            user_id = update.callback_query.from_user.id

        if user_id not in authenticated_users:
            logger.warning(f"Unauthorized access attempt by user {user_id}")
            if update.message:
                await update.message.reply("You are not authorized to use this bot.")
            elif update.callback_query:
                await update.callback_query.answer(text="You are not authorized to use this bot.", show_alert=True)
            raise Dispatcher.handler.stop()

class RateLimitMiddleware(BaseMiddleware):
    """
    Middleware for rate limiting.
    """
    async def on_process_update(self, update: Update, data: Dict[str, Any]):
        """
        Apply rate limiting to the user before processing the update.

        Args:
            update (Update): The incoming update.
            data (Dict[str, Any]): The data dictionary.
        """
        user_id = None
        if update.message:
            user_id = update.message.from_user.id
        elif update.callback_query:
            user_id = update.callback_query.from_user.id

        current_time = time.time()
        last_request_time = user_request_times.get(user_id, 0)

        if current_time - last_request_time < 1.0:  # 1 second rate limit
            logger.warning(f"Rate limit exceeded for user {user_id}")
            if update.message:
                await update.message.reply("Please wait before sending another message.")
            elif update.callback_query:
                await update.callback_query.answer(text="Please wait before sending another request.", show_alert=True)
            raise Dispatcher.handler.stop()

        user_request_times[user_id] = current_time


'''
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)

    # Register middlewares
    dp.update.middleware(LoggingMiddleware())
    dp.update.middleware(AuthMiddleware())
    dp.update.middleware(RateLimitMiddleware())

    # Handler for the /start command
    @dp.message(commands=['start'])
    async def send_welcome(message: types.Message):
        """
        Sends a welcome message to the user.

        Args:
            message (types.Message): The message object.
        """
        await message.reply("Welcome! You are authorized to use this bot.")

    # Handler for text messages
    @dp.message()
    async def echo(message: types.Message):
        """
        Echoes the user's message back to them.
        
        Args:
        message (types.Message): The message object.
        """
        await message.reply(f"You said: {message.text}")
'''