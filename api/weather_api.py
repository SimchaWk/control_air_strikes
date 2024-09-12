import requests
from typing import Dict, Any, Optional
from toolz import pipe, curry
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"


@curry
def api_request(url: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    try:
        return pipe(
            requests.get(url, params=params),
            lambda response: response.raise_for_status() or response.json()
        )
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


get_full_weather_data = api_request(BASE_URL)
