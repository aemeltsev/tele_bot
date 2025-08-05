import requests as req
import logging
#from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

@dataclass
class DayWeather:
    '''
    A dataclass to hold weather data for specific times of a day.
    '''
    #0-night(1h), 1-morning(7h), 2-day(14h), 3-evening(19h)
    time:list[str]
    temperature_2m:list[float] 
    relative_humidity_2m:list[int]
    apparent_temperature:list[float]
    precipitation:list[int]
    rain:list[float]
    showers:list[float]
    snowfall:list[float]
    weather_code:list[str]
    pressure_msl:list[float]
    surface_pressure:list[float]
    cloud_cover:list[int]
    wind_speed_10m:list[float]
    wind_direction_10m:list[int]
    wind_gusts_10m:list[float]

class WeatherForecast:
    '''
    A class to fetch and process weather forecast data from the Open-Meteo API - https://open-meteo.com.

    This class provides methods to retrieve weather forecast data for a given latitude and longitude.
    It uses the Open-Meteo API to fetch hourly weather data and processes it into a more usable format.

    Attributes:
        url (str): The base URL for the Open-Meteo API.
        lon (float): The longitude for the location to fetch weather data.
        lat (float): The latitude for the location to fetch weather data.
        current (str): A string of comma-separated weather parameters to fetch from the API.

    For more information, see the Open-Meteo API documentation: https://open-meteo.com/en/docs

    Example:
        >>> weather_forecast = WeatherForecast(lon=38.5, lat=52.62)
        >>> forecast_data = weather_forecast.quest(forecast_day=3)
        >>> for day in forecast_data:
        ...     print(day)
    '''

    url: str = 'https://api.open-meteo.com/v1/forecast'
    '''
    url: The base URL for the Open-Meteo API.
    '''    
    current: str = 'temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,rain,showers,snowfall,weather_code,cloud_cover,pressure_msl,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m'
    '''
    current: A string of comma-separated weather parameters to fetch from the API.
    '''

    weather_code_dict_en = {
        0 : 'clear sky \U00002600 ', # ясно 
        1 : 'mainly clear \U00002600 ', # преимущественно ясно 
        2 : 'partly cloudy \U000026C5 ', # переменная облачность 
        3 : 'overcast \U00002601 ', # пасмурно
        45 : 'fog \U00001F32B ', # туман
        48 : 'depositing rime fog ', # отложения инейного тумана
        51 : 'drizzle: light intensity \U00004204 ', # морось легкая
        53 : 'drizzle: moderate intensity \U00004204 ', # морось умеренная
        55 : 'drizzle: dense intensity \U00004204 ', # морось плотная
        56 : 'freezing drizzle: light intensity \U0001F326 ', # моросящий дождь: легкий
        57 : 'freezing drizzle: dense intensity \U0001F326 ', # моросящий дождь: плотный
        61 : 'rain: light intensity \U0001F326 ', # дождь: слабый
        63 : 'rain: moderate intensity \U0001F326 ', # дождь: умеренный
        65 : 'rain: heavy intensity \U0001F326 ', # дождь: сильный
        66 : 'freezing rain: light intensity ', # ледяной дождь: легкая интенсивность
        67 : 'freezing rain: heavy intensity ', # ледяной дождь: сильная интенсивность
        71 : 'snow fall: slight intensity \U00002744 ', # снегопад: слабый
        73 : 'snow fall: moderate intensity \U0001F328 ', # снегопад: умеренный
        75 : 'snow fall: heavy intensity \U0001F328 ', # снегопад: сильный
        77 : 'snow grains ', # снежные зерна
        80 : 'rain showers: slight \U0001F327 ', # ливни: слабые
        81 : 'rain showers: moderate \U0001F327 ', # ливни: умеренные
        82 : 'rain showers: violent \U0001F327 ', # ливни: сильные
        85 : 'snow showers slight ', # снежные ливни слабые
        86 : 'snow showers heavy ', # снежные ливни сильные
        95 : 'thunderstorm: slight or moderate \U000026C8 ', # гроза: слабая или умеренная
        96 : 'thunderstorm with slight hail \U000026A1 ', # гроза с небольшим градом
        99 : 'thunderstorm with heavy hail \U000026A1 ' # гроза с сильным градом
    }

    def __init__(self, lon: float, lat: float) -> None:
        '''
        Initialize the WeatherForecast class with longitude and latitude.

        Args:
            lon (float): The longitude for the location to fetch weather data.
            lat (float): The latitude for the location to fetch weather data.
        '''
        logger.info(f'Initialise WeatherForecast class with lon={lon}, lat={lat}')
        self.lon = lon
        self.lat = lat

    def _make_request(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        '''
        Helper method to make the API request and handle the response.

        Args:
            params (Dict[str, Any]): Parameters for the API request.

        Returns:
            Optional[Dict[str, Any]]: The JSON response from the API or None if the request fails.
        '''
        response = req.get(url=self.url, params=params)

        logger.info(f'The request to {self.url} has been made with parameters: {params}')
        if response.status_code != req.codes.ok:
            logger.error('The request failed with status code %s', response.status_code)
            return None
        logger.info('The request was successful')
        return response.json()
    
    def _create_day_weather(self, forecast: Dict[str, Any], start_index: int) -> DayWeather:
        '''
        Helper method to create a DayWeather object from the forecast data.

        Args:
            forecast (Dict[str, Any]): The forecast data from the API.
            start_index (int): The starting index for the hourly data.

        Returns:
            DayWeather: A DayWeather object containing the weather data for specific times of a day.
        '''
        time_indices = [start_index + 1, start_index + 7, start_index + 14, start_index + 19]
        return DayWeather(
            time=[forecast['hourly']['time'][i] for i in time_indices],
            temperature_2m=[forecast['hourly']['temperature_2m'][i] for i in time_indices],
            relative_humidity_2m=[forecast['hourly']['relative_humidity_2m'][i] for i in time_indices],
            apparent_temperature=[forecast['hourly']['apparent_temperature'][i] for i in time_indices],
            precipitation=[forecast['hourly']['precipitation'][i] for i in time_indices],
            rain=[forecast['hourly']['rain'][i] for i in time_indices],
            showers=[forecast['hourly']['showers'][i] for i in time_indices],
            snowfall=[forecast['hourly']['snowfall'][i] for i in time_indices],
            weather_code=[self.weather_code_dict_en[forecast['hourly']['weather_code'][i]] for i in time_indices],
            pressure_msl=[forecast['hourly']['pressure_msl'][i] for i in time_indices],
            surface_pressure=[forecast['hourly']['surface_pressure'][i] for i in time_indices],
            cloud_cover=[forecast['hourly']['cloud_cover'][i] for i in time_indices],
            wind_speed_10m=[forecast['hourly']['wind_speed_10m'][i] for i in time_indices],
            wind_direction_10m=[forecast['hourly']['wind_direction_10m'][i] for i in time_indices],
            wind_gusts_10m=[forecast['hourly']['wind_gusts_10m'][i] for i in time_indices]
        )
    
    def quest(self, forecast_day: int = 3) -> Optional[List[DayWeather]]:
        '''        
        Fetch weather forecast data from the Open-Meteo API.

        https://api.open-meteo.com/v1/forecast?
        latitude=00.0000&longitude=00.0000&
        hourly=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation_probability,
        rain,showers,snowfall,weather_code,pressure_msl,surface_pressure,cloud_cover,
        wind_speed_10m,wind_direction_10m,wind_gusts_10m&
        timezone=auto&
        forecast_days=3

        This method constructs a request to the Open-Meteo API with the specified parameters,
        sends the request, and processes the response into a list of DayWeather objects.

        Args:
            forecast_day (int, optional): The number of forecast days to retrieve. Defaults to 3.

        Returns:
            Optional[List[DayWeather]]: A list of DayWeather objects containing the weather forecast data,
                                        or None if the request fails.
        '''
        
        logger.info('Fetching weather data from Open-Meteo API...')
        method = {
            'latitude':str(self.lat),
            'longitude':str(self.lon),
            'hourly':self.current,
            'timezone':'auto',
            'forecast_days':str(forecast_day)
        }
        return self._make_request(method)
    
    def create_forecast(self, forecast: Dict[str, Any]) -> Optional[List[DayWeather]]:
        '''
        Create a list of DayWeather objects from the forecast data.
        
        Args:
            forecast (Dict[str, Any]): The forecast data from the API.
        
        Returns:
            Optional[List[DayWeather]]: A list of DayWeather objects or None if the data is invalid.
        '''
        first_day = self._create_day_weather(forecast, 0)
        second_day = self._create_day_weather(forecast, 24)
        third_day = self._create_day_weather(forecast, 48)
        
        return [first_day, second_day, third_day]