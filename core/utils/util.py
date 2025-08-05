import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple

def extract_lat_lon(data: Dict[str, Any]) -> Tuple[Optional[float], Optional[float]]:
    """Helper method to extract latitude and longitude from JSON data."""
    if data and 'lat' in data and 'lon' in data:
        return data['lat'], data['lon']
    return None, None

def generate_token_hash(token: str) -> str:
    """Generate a SHA-256 hash of the given token."""
    return hashlib.sha256(token.encode()).hexdigest()

def is_forecast_old(timestamp: datetime) -> bool:
    """Check if the given timestamp is older than 12 hours."""
    return datetime.now() - timestamp > timedelta(hours=12)