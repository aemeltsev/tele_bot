import requests as req
import json
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class Geocode:
    '''
    A utility class for converting between geographic coordinates and addresses using the Geocode.maps.co API.

    This class provides functionality to convert a given user address into geographic coordinates
    (latitude and longitude key code_search=True - direct conversion) and vice versa.
    It leverages the Geocode.maps.co service API to perform these conversions efficiently and accurately.

    Attributes:
        url (str): The base URL for the Geocode.maps.co API.
        api_key (str): The API key for accessing the Geocode.maps.co service.
        qtype (bool): A flag indicating the type of conversion.
                      If True, converts an address to coordinates (direct conversion).
                      If False, converts coordinates to an address (reverse conversion).
        search (str): The endpoint for direct conversion (address to coordinates).
        reverse (str): The endpoint for reverse conversion (coordinates to address).

    Methods:
        __init__(self, url: str, code_search: bool = True, api_key: str = 'TOKEN') -> None:
            Initializes the Geocode class with the specified URL, conversion type, and API key.

        quest(self, address: str = 'unknown', lat: float = 0.0, lon: float = 0.0) -> Optional[dict]:
            Performs the geocode conversion based on the specified parameters.
            For direct conversion (address to coordinates), provide the address.
            For reverse conversion (coordinates to address), provide the latitude and longitude.
            Returns a dictionary with the conversion results or None if the request fails.
    '''

    def __init__(self, url: str, code_search: bool = True, api_key: str = 'TOKEN') -> None:
        self.url = url
        self.qtype = code_search
        self.api_key = api_key
        self.search = '/search'
        self.reverse = '/reverse'

    def _make_request(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        '''
        Helper method to make the API request and handle the response.
        '''
        response = req.get(url=self.url, params=params)
        if response.status_code != req.codes.ok:
            return None
        return response.json()
    
    def _safe_to_file(self, data: Dict[str, Any], filename: str) -> None:
        '''
        Helper method to save data to a file.
        '''
        try:
            with open(f'files/data/{filename}.json', 'w') as f:
                json.dump(data, f)
        except IOError as e:
            logger.error(f'An error occurred while writing to the file: {e}')
        
    def quest(self, addres: str = 'unknown', lat: float = 0.0, lon: float = 0.0) -> Optional[Dict[str, Any]]:
        '''
        Geocode question, for example search the coordinates by the city name:
            1. url=https://geocode.maps.co.
            2. search=/search.
            3. address= transform to q=address&.
            4. result url='https://geocode.maps.co/search?q=address&api_key=api_key'.
        after check request status code and save the json data to file.
        '''
        out = {}

        if self.qtype:
            self.url += self.search
            method = {'q':addres, 'api_key': self.api_key}
        else:
            self.url += self.reverse
            method = {'lat': str(lat), 'lon': str(lon), 'api_key': self.api_key}
        
        geo_data = self._make_request(method)
        if not geo_data:
            logger.error('The Geo data is empty. Please check the API key and the request parameters.')
            return None
        
        if self.qtype:
            out['address'] = str(geo_data[0]['display_name']).split(', ')[0]
            out['lat'] = round(float(geo_data[0]['lat']), 2)
            out['lon'] = round(float(geo_data[0]['lon']), 2)
        else:
            out['address'] = str(geo_data.get('address', {}).get('city', 'unknown'))
            out['lat'] = round(float(geo_data.get('lat', 0.0)), 2)
            out['lon'] = round(float(geo_data.get('lon', 0.0)), 2)

        var_dict: dict = out
        addr = var_dict['address']
        self._safe_to_file(var_dict, addr) 
        return out
