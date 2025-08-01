'''
Basic handlers for registration
'''
import os
import logging
import secrets

from dotenv import load_dotenv

from aiogram import Bot
from aiogram.types import Message
from aiogram.filters import CommandObject
from typing import Optional, Dict, Any

from sqlalchemy.orm import Session
from core.model.models import SessionLocal, User

from core.utils.geocode import Geocode
from core.utils.weather import WeatherForecast, DayWeather
from core.utils.util import get_json_data, extract_lat_lon

logger = logging.getLogger(__name__)

load_dotenv()

# Временное хранилище для токенов
tokens = {}

def get_db():
    '''
    Dependency to get the database session
    '''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def check_authorization(message: Message):
    user_id = message.from_user.id
    db: Session = next(get_db())
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            await message.reply("Sorry you dont have access to this bot.")
            return False
        return True
    except Exception as e:
        await message.reply(f'Sorry, have some problem - {e}')
        logger.error(f'Exception with autorization : {e}')
    finally:
        db.close()

async def cmd_start(message: Message, bot: Bot):
    """Handler for the /start command."""

    if not await check_authorization(message):
        return

    welcome_message = f"""
    Hello {message.from_user.first_name}! Nice to meet you! \U00002600
    
    Welcome to the Weather Bot! I'm here to help you get the latest weather updates for any city around the world.
    
    Here are a few things you can do:
    - Get weather forecasts by typing /weather followed by the city name. For example, /weather Moscow.
    - Use the /help command to get more information about the available commands and how to use them.
    
    If you have any questions or need assistance, feel free to ask!
    """
    await bot.send_message(message.from_user.id, welcome_message)
    logger.info(f'User {message.from_user.first_name} with ID {message.from_user.id} started the bot.')

async def cmd_help(message: Message):
    """Handler for the /help command."""

    if not await check_authorization(message):
        return

    help_text: str = """
    Here are the available commands and their descriptions:
    
    /start - Welcome message and initial interaction with the bot.
        Usage: Just type /start to begin.
    
    /help - Displays this help message with information about available commands.
        Usage: Type /help to see this message.
        
    /weather - Get the weather forecast for a specific location.
        Usage: Type /weather followed by the city name. For example, /weather Moscow.
        Note: Make sure to provide the city name correctly for accurate results.
        
    If you have any questions or need further assistance, feel free to ask!
    """
    await message.reply(help_text)
    logger.info(f'User {message.from_user.first_name} with ID {message.from_user.id} requested help.')

async def get_geocode_location(name: str) -> Optional[Dict[str, Any]]:
    """Helper method to get geocode location."""
    geo_token = os.getenv('GEOCODE_TOKEN')
    data = get_json_data(name + '.json')
    if data:
        lat, lon = extract_lat_lon(data)
        if lat is not None and lon is not None:
            logger.info(f'Geocode location from file for {name} is {lat}, {lon}.')
            return {'address': name, 'lat': lat, 'lon': lon}

    geocode_location = Geocode(url='https://geocode.maps.co', code_search=True, api_key=geo_token)
    location = geocode_location.quest(name)
    logger.info(f'Geocode location from API request - {location}')
    if location is None:
        return None
    return location

async def get_weather_forecast(lat: float, lon: float) -> Optional[list[DayWeather]]:
    """Helper method to get weather forecast."""
    weather_forecast = WeatherForecast(lon, lat).quest()
    if weather_forecast is None:
        return None
    return weather_forecast

async def send_weather_message(message: Message, weather_forecast: list[DayWeather]) -> None:
    """Helper method to send weather messages."""
    for day in weather_forecast:
        for i, time in enumerate(day.time):
            await message.answer(f'Time: {time}, Temperature: {day.temperature_2m[i]}, Forecast: {day.weather_code[i]}')

async def cmd_weather(message: Message, command: CommandObject) -> None:
    """Handler for the /weather command."""

    if not await check_authorization(message):
        return

    if command.args is None:
        await message.answer("Error, no arguments passed. Pass the city name.")
        return
    
    name = command.args
    # TODO write the name of the settlement to a database
    # TODO subsequently check, in a file or database, the presence of a geographic point and therefore coordinates
    location = await get_geocode_location(name)
    if location is None:
        await message.answer("Error, unknown location arguments passed.")
        return
    
    lat, lon = location["lat"], location["lon"]
    # TODO: Record the coordinates for the current city in database

    weather_forecast = await get_weather_forecast(lat, lon)
    if weather_forecast is None:
        await message.answer("Error, don't get data of weather forecast.")
        return
    
    await send_weather_message(message, weather_forecast)


async def cmd_login(message: Message) -> None:
    """Handler for the /login command."""
    user_id = message.from_user.id
    db: Session = next(get_db())
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            await message.answer("You are already logged in.")
            return
        
        # A hash of the token is generated and stored in the temporary `tokens` storage.
        token = secrets.token_urlsafe(32)
        token_hash = generate_token_hash(token)
        tokens[user_id] = token_hash
        await message.reply(f'Your temporary token:\n {token}\n Use command /signup <token> to login.')
    except Exception as e:
        await message.reply(f'An error occurred: {e}')
        logger.info(f'An error occurred: {e}')
    finally:
        db.close()

async def cmd_signup(message: Message, command: CommandObject) -> None:
    """Handler for the /signup command."""
    user_id = message.from_user.id
    token = command.args
    if not token:
        await message.reply("Error, token is not passed.")
        return
    '''
    A hash is generated from the token provided by the user and compared with the stored hash. 
    If the hashes match, the user is authorized.
    '''
    token_hash = generate_token_hash(token)
    if tokens.get(user_id) != token_hash:
        await message.reply("Error, invalid token.")
        return

    db: Session = next(get_db())
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            user = User(user_id=user_id, token=token_hash)
            db.add(user)
            db.commit()
            await message.reply('You have successfully logged in.')
        else:
            await message.reply('You are already logged in.')
    except Exception as e:
        await message.reply(f'An error occurred: {e}')
    finally:
        db.close()