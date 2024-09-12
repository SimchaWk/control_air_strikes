import json
from functools import partial
from typing import List, Dict, Any, Optional
from toolz import pipe, get_in
from models.aircraft import Aircraft
from models.pilot import Pilot
from models.target import Target
from service.weather_service import collect_weather_data


def load_pilots_from_json(file_path: str) -> List[Pilot]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return [Pilot(name=pilot['name'], skill_level=pilot['skill']) for pilot in data['pilots']]

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return []


def load_aircrafts_from_json(file_path: str) -> List[Aircraft]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return [
            Aircraft(ac_type=aircraft['type'], speed=aircraft['speed'], fuel_capacity=aircraft['fuel_capacity'])
            for aircraft in data['aircrafts']
        ]

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return []


def load_targets_from_json(file_path: str) -> List[Target]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return [Target(city=target['city'], priority=target['priority']) for target in data['targets']]

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return []


def load_location_city_from_json(file_path: str, city: str) -> Optional[tuple]:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return get_in([city, 'location', 'lat'], data), get_in([city, 'location', 'lon'], data)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None


def write_to_json(data: Dict[str, Any], file_path: str) -> None:
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def save_weather_and_location_data_to_json(cities: List[str], file_path: str = 'weather_data.json') -> None:
    pipe(
        cities,
        collect_weather_data,
        partial(write_to_json, file_path=file_path)
    )
