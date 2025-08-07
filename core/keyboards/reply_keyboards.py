from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List, Optional

# Constants for button texts
OPTION_A = "Option A"
OPTION_B = "Option B"

def get_reply_keyboard(
    buttons: Optional[List[str]] = None,
    resize_keyboard: bool = True,
    one_time_keyboard: bool = True
) -> ReplyKeyboardMarkup:
    """
    Creates and returns a reply keyboard markup with predefined or custom buttons.

    Args:
        buttons (Optional[List[str]]): List of button texts. If None, default buttons are used.
        resize_keyboard (bool): Whether to resize the keyboard.
        one_time_keyboard (bool): Whether to hide the keyboard after use.

    Returns:
        ReplyKeyboardMarkup: A reply keyboard markup with the specified buttons.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard)

    # Use default buttons if none are provided
    if buttons is None:
        buttons = [OPTION_A, OPTION_B]

    # Add buttons to the keyboard
    keyboard.add(*[KeyboardButton(button) for button in buttons])

    return keyboard


'''
    Example usage:
    
    # Handler for the /start command
    @dp.message(commands=['start'])
    async def send_welcome(message: types.Message):
    """
    Sends a welcome message with a reply keyboard.

    Args:
        message (types.Message): The message object.
    """
        keyboard = get_reply_keyboard()
        await message.reply("Welcome! Please choose an option:", reply_markup=keyboard)

    # Handler for Option A
    @dp.message(lambda message: message.text == OPTION_A)
    async def handle_option_a(message: types.Message):
    """
    Handles the user's choice of Option A.

    Args:
        message (types.Message): The message object.
    """
        await message.reply("You chose Option A.")

    # Handler for Option B
    @dp.message(lambda message: message.text == OPTION_B)
    async def handle_option_b(message: types.Message):
    """
    Handles the user's choice of Option B.

    Args:
        message (types.Message): The message object.
    """
        await message.reply("You chose Option B.")
'''