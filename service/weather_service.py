from datetime import datetime, timedelta
from functools import partial
from typing import Optional, List, Dict, Any
from toolz import get_in, pipe
from api.weather_api import get_full_weather_data
API_KEY = "8971ae449e424802bbd2b30c412b1655"


def get_target_time(target_time: Optional[datetime] = None) -> datetime:
    return target_time or (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1))


def find_closest_forecast(forecasts: List[Dict[str, Any]], target_time: datetime) -> Dict[str, Any]:
    target_timestamp = int(target_time.timestamp())
    return min(forecasts, key=lambda x: abs(x['dt'] - target_timestamp))


def extract_location(data: Dict[str, Any]) -> Dict[str, float]:
    return {
        "lat": get_in(['city', 'coord', 'lat'], data),
        "lon": get_in(['city', 'coord', 'lon'], data)
    }


def extract_weather(forecast: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "weather": get_in(['weather', 0, 'main'], forecast),
        "clouds": get_in(['clouds', 'all'], forecast),
        "wind_speed": get_in(['wind', 'speed'], forecast)
    }


def extract_weather_info(full_data: Optional[Dict[str, Any]], target_time: Optional[datetime] = None)\
        -> Optional[Dict[str, Any]]:
    if not full_data or 'list' not in full_data:
        return None

    return {
        "location": extract_location(full_data),
        "weather": pipe(
            full_data['list'],
            partial(find_closest_forecast, target_time=get_target_time(target_time)),
            extract_weather
        )
    }


def get_weather_for_midnight(api_key: str, city: str, target_time: Optional[datetime] = None)\
        -> Optional[Dict[str, Any]]:
    return pipe(
        get_full_weather_data({'q': city, 'appid': api_key, 'units': 'metric'}),
        partial(extract_weather_info, target_time=target_time)
    )


def collect_weather_data(cities: List[str]) -> Dict[str, Any]:
    return pipe(
        cities,
        lambda cities: map(partial(get_weather_for_midnight, API_KEY), cities),
        lambda data: {city: weather for city, weather in zip(cities, data) if weather}
    )
