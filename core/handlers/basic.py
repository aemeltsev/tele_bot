'''
Basic handlers for registration
'''
import os
import logging
import secrets

from dotenv import load_dotenv

from datetime import datetime

from aiogram import Bot
from aiogram.types import Message
from aiogram.filters import CommandObject
from typing import Optional, Dict, Any

from sqlalchemy.orm import Session
from core.model.models import SessionLocal, User, City, Forecast

from core.utils.geocode import Geocode
from core.utils.weather import WeatherForecast, DayWeather
from core.utils.util import extract_lat_lon, generate_token_hash, is_forecast_old

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

### CRUD functions for User
def create_user(db: Session, user_id: int, token: str):
    '''
    Add user to database
    '''
    db_user = User(user_id=user_id, token=token)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    '''
    Get user from database
    '''
    return db.query(User).filter(User.user_id == user_id).first()

def update_user(db: Session, user_id: int, token: str, is_active=None):
    '''
    Update user token in database
    '''
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        if token is not None:
            db_user.token = token
        if is_active is not None:
            db_user.is_active = is_active
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    '''
    Delete user from database
    '''
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user
### CRUD functions for User

### CRUD functions for City
def create_city(db: Session, user_id: int, name: str, latitude: float, longitude: float):
    '''
    Add city to database
    '''
    db_city = City(user_id=user_id, name=name, latitude=latitude, longitude=longitude)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def get_city_coordinates(db: Session, name: str):
    '''
    Get city coordinates from the database.

    Args:
        db (Session): Database session.
        name (str): Name of the city.

    Returns:
        Optional[Dict[str, float]]: A dictionary containing the city's name, latitude, and longitude.
            Returns None if the city is not found or an error occurs.
    '''
    if not name:
        logger.error("City name is empty")
        return None
    
    try:
        db_city = db.query(City).filter(City.name == name).first()
        if db_city:
            return {
                "name": db_city.name,
                'latitude': db_city.latitude,
                'longitude': db_city.longitude
            }
        else:
            logger.error(f"City {name} not found in the database")
            return None
    except Exception as e:
        logger.error(f'Error getting city coordinates: {e}')
        return None

def get_city_id_by_name(db: Session, city_name: str) -> Optional[int]:
    ''' Get city by name from the database.'''
    try:
        db_city = db.query(City).filter(City.name == city_name).first()
        return db_city.id
    except Exception as e:
        logger.error(f"Error querying city ID by name: {e}")
        return None

# Maybe unused
def get_city_name(db: Session, latitude: float, longitude: float):
    '''
    Get city name from the database based on latitude and longitude.

    Args:
        db (Session): Database session.
        latitude (float): Latitude of the city.
        longitude (float): Longitude of the city.

    Returns:
        Optional[str]: Name of the city if found, otherwise None.
    '''
    try:
        # Validate input parameters
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            logger.error("Invalid latitude or longitude values.")
            return None
        
        # Query the database for the city name
        db_city = db.query(City).filter(
            City.latitude == latitude,
            City.longitude == longitude
        ).first()
        
        if db_city:
            logger.info(f'City found: {db_city.name}')
            return db_city.name
        else:
            logger.warning(f'No city found at latitude {latitude} and longitude {longitude}.')
            return None
    except Exception as e:
        logger.error(f'Error querying city by coordinates: {e}')
        return None
### CRUD functions for City

### CRUD functions for Forecast
def get_weather_forecast_by_city_id(db: Session, city_id: int) -> Optional[Forecast]:
    '''
    Get weather forecast by city ID from the database.
    '''
    try:
        db_forecast = db.query(Forecast).filter(Forecast.city_id == city_id).first()
        return db_forecast
    except Exception as e:
        logger.error(f"Error querying weather forecast by city ID: {e}")
        return None

def create_or_update_weather_forecast(db: Session, city_id: int, forecast_data: dict) -> Optional[Forecast]:
    '''
    Create or update a weather forecast entry in the database.

    :param db: SQLAlchemy database session
    :param city_id: ID of the city for which the forecast is being created
    :param forecast_data: Dictionary containing weather forecast data
    :return: Created Forecast object
    '''
    try:
        forecast = get_weather_forecast_by_city_id(db, city_id)
        if forecast:
            forecast.forecast_data = forecast_data
            forecast.timestamp = datetime.now()
        else:
            forecast = Forecast(city_id=city_id, forecast_data=forecast_data)
            # Add the new instance to the database
            db.add(forecast)
        # Commit the session to save the new forecast to the database
        db.commit()
        # Refresh the instance to get any new data from the database
        db.refresh(forecast)
        return forecast
    except Exception as e:
        logger.error(f"Error creating or updating weather forecast: {e}")
        db.rollback()
        return None
### CRUD functions for Forecast

async def fetch_weather_from_api(lat: float, lon: float) -> Optional[dict]:
    '''
    Fetch weather data from the OpenWeatherMap API.
    '''
    try:
        weather_data = WeatherForecast(lon, lat).quest()
        if weather_data is None:
            logger.error("Failed to fetch weather data from API")
        return weather_data
    except Exception as e:
        logger.error(f"Error fetching weather data from API: {e}")
        return None

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
        await message.reply("Sorry, an internal authorization error occurred.")
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
    
    /start - Welcome message and initial interaction with the bot.\n
    Usage: Just type /start to begin.

    /login - Log in to the bot.\n
    Usage: Enter /login to get a registration token.
    
    /signup - Sign up for the bot.\n
    Usage: Enter /signup <token> to register.
    
    /help - Displays this help message with information about available commands.\n
    Usage: Type /help to see this message.
        
    /weather - Get the weather forecast for a specific location.\n
    Usage: Type /weather followed by the city name. For example, /weather Moscow.\n
    Note: Make sure to provide the city name correctly for accurate results.
        
    If you have any questions or need further assistance, feel free to ask!
    """
    await message.reply(help_text)
    logger.info(f'User {message.from_user.first_name} with ID {message.from_user.id} requested help.')

async def get_geocode_location(message: Message, address: str) -> Optional[Dict[str, Any]]:
    """Helper method to get geocode location."""
    gtoken = os.getenv('GEOCODE_TOKEN')
    db: Session = next(get_db())
    logger.info("Query of location coordinates from DB")
    data = get_city_coordinates(db, address)

    if data:
        lat, lon = extract_lat_lon(data)
        if lat is not None and lon is not None:
            logger.info(f'Geocode location from file for {address} is {lat}, {lon}.')
            return {'address': address, 'lat': lat, 'lon': lon}

    logger.info("Query of location coordinates from API")
    geocode_location = Geocode(url='https://geocode.maps.co', code_search=True, api_key=gtoken)
    location = geocode_location.quest(address)
    logger.info(f'Geocode location from API request - {location}')

    if location is not None:
        user_id = message.from_user.id
        create_city(db, user_id, address, location['lat'], location['lon'])
        print("location is exist")
        return location
    return None

async def get_weather_forecast(name: str, lat: float, lon: float) -> Optional[list[DayWeather]]:
    """Helper method to get weather forecast."""
    db: Session = next(get_db())
    try:
        logger.info("Query of forecast from DB")
        
        # Get the city ID from the database using the city name
        city_id = get_city_id_by_name(db, name)
        if city_id is None:
            # Fix it later: get city id from geocode
            logger.info(f"City {name} not found in the database.")
            return None
    
        # Query the weather forecast for the city using the city ID
        forecast = get_weather_forecast_by_city_id(db, city_id)

        # If the forecast is not found or older than 12 hours, fetch it from the API
        if forecast is None or is_forecast_old(forecast.timestamp):
            logger.info(f"Weather forecast for city {name} not found in the database. Fetching from API...")
            # Get the weather forecast from the API
            weather_data = await fetch_weather_from_api(lat=lat, lon=lon)
            if weather_data is None:
                logger.info("Failed to fetch weather forecast from API.")
                return None
        
            # Create a new forecast entry in the database
            forecast = create_or_update_weather_forecast(db, city_id, weather_data)
            if forecast is None:
                return None
    
        # Assuming forecast.forecast_data is a dictionary that can be converted to DayWeather objects
        weather_forecast = WeatherForecast(lon, lat).create_forecast(forecast.forecast_data)
        return weather_forecast
    
    finally:
        db.close()

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
    location = await get_geocode_location(message, name)
    if location is None:
        await message.answer("Error, unknown location arguments passed.")
        return
    
    lat, lon = location["lat"], location["lon"]
    
    weather_forecast = await get_weather_forecast(name, lat, lon)
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