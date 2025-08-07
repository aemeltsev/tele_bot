from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData

# Define callback data for city selection
city_callback = CallbackData("city", "city_id")

def get_cities_keyboard(cities: list) -> InlineKeyboardMarkup:
    """
    Creates and returns an inline keyboard markup for city selection.

    Args:
        cities (list): List of city names.

    Returns:
        InlineKeyboardMarkup: An inline keyboard markup with city options.
    """
    keyboard = InlineKeyboardMarkup()
    for city_id, city_name in enumerate(cities, start=1):
        keyboard.add(InlineKeyboardButton(
            text=city_name,
            callback_data=city_callback.new(city_id=city_id)
        ))
    return keyboard


'''
    Example usage:
    
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot)
    # Sample weather data
    weather_data = {
        1: {"city": "New York", "temperature": 70, "condition": "Sunny"},
        2: {"city": "London", "temperature": 60, "condition": "Cloudy"},
        3: {"city": "Tokyo", "temperature": 75, "condition": "Rainy"},
    }

    # List of cities
    cities = ["New York", "London", "Tokyo"]

    # Handler for the /start command
    @dp.message(commands=['start'])
    async def send_welcome(message: types.Message):
    """
    Sends a welcome message and presents the city selection keyboard.

    Args:
        message (types.Message): The message object.
    """
        keyboard = get_cities_keyboard(cities)
        await message.reply("Welcome to the Weather Bot! Please select a city:", reply_markup=keyboard)

    # Handler for city selection callbacks
    @dp.callback_query(city_callback.filter())
    async def handle_city_selection(call: types.CallbackQuery, callback_data: dict):
    """
    Handles the user's city selection from the inline keyboard.

    Args:
        call (types.CallbackQuery): The callback query object.
        callback_data (dict): The callback data.
    """
        city_id = int(callback_data["city_id"])
        city_weather = weather_data[city_id]

        await bot.answer_callback_query(call.id)
        await bot.send_message(
            call.from_user.id,
            f"Weather in {city_weather['city']}: {city_weather['temperature']}°F, {city_weather['condition']}"
        )
'''