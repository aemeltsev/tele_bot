import os
import json
from typing import Dict, Any, Optional, Tuple

def get_json_data(filename: str) -> Optional[Dict[str, Any]]:
    # Get the list of all files in the current directory
    files = os.listdir()

    # Find file with the given filename and .JSON extension
    for file in files:
        if file == filename and file.endswith('.json'):
            # Open the file and load the JSON data
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        
    # If file not found, return None
    return None

def extract_lat_lon(data: Dict[str, Any]) -> Tuple[Optional[float], Optional[float]]:
    """Helper method to extract latitude and longitude from JSON data."""
    if data and 'lat' in data and 'lon' in data:
        return data['lat'], data['lon']
    return None, None