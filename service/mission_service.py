import math
from functools import partial
from itertools import product
from typing import List, Dict
from toolz import pipe, curry, unique
from models.aircraft import Aircraft
from models.pilot import Pilot
from models.target import Target
from repository.json_repository import load_location_city_from_json


weights = {
    "distance": 0.20,
    "aircraft _ type": 0.25,
    "pilot skill": 0.25,
    "weather conditions": 0.20,
    "execution time": 0.10
}

weather_score = {
    'Clear': 1.0,
    'clouds': 0.7,
    'Rain': 0.4,
    'Stormy': 0.2
}


def get_weather_score(weather: str) -> float:
    return weather_score[weather] if weather in weather_score else 0


def compute_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    return math.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)


def compute_distance_from_tel_aviv(lat: float, lon: float) -> float:
    TLV_LAT, TLV_LON = 32.0853, 34.7818
    return compute_distance(lat, lon, TLV_LAT, TLV_LON)


def get_distance_per_target(target: Target) -> float:
    cities_coords = load_location_city_from_json(
        'C:/Users/Simch/PycharmProjects/control_air_strikes/repository/files/weather_data.json',
        target.city
    )
    return compute_distance_from_tel_aviv(cities_coords[0], cities_coords[1])


def update_target_distance(target: Target) -> Target:
    target.distance = get_distance_per_target(target)
    return target


def update_target_weather_score(target: Target) -> Target:
    target.weather_score = 0
    return target


def calculate_weather_score(weather_data):
    cloud_cover = weather_data.get('clouds', {}).get('all', 0)
    wind_speed = weather_data.get('wind', {}).get('speed', 0)
    rain = weather_data.get('rain', {}).get('1h', 0)

    cloud_score = max(0, 100 - cloud_cover)

    if wind_speed < 10:
        wind_score = 100 - (wind_speed * 5)
    else:
        wind_score = max(0, 100 - (wind_speed * 10))

    rain_score = max(0, 100 - (rain * 50))

    final_score = (cloud_score + wind_score + rain_score) / 3

    return round(final_score, 2)


def generate_mission_combinations(
        targets: List[Target],
        aircraft: List[Aircraft],
        pilots: List[Pilot]
) -> List[Dict]:

    combinations = []

    for target, plane, pilot in product(targets, aircraft, pilots):
        combination = {
            'target': {
                'city': target.city,
                'priority': target.priority,
                'weather_score': target.weather_score,
                'distance': target.distance
            },
            'aircraft': {
                'type': plane.type,
                'speed': plane.speed,
                'fuel_capacity': plane.fuel_capacity
            },
            'pilot': {
                'name': pilot.name,
                'skill_level': pilot.skill_level
            }
        }
        combinations.append(combination)

    return combinations


@curry
def calculate_mission_score(mission: Dict[str, Dict]) -> float:

    target = mission['target']
    aircraft = mission['aircraft']
    pilot = mission['pilot']

    weights = {
        'distance': 0.20,
        'aircraft': 0.25,
        'pilot_skill': 0.25,
        'weather': 0.20,
        'execution_time': 0.10
    }

    distance_score = 1 - (target['distance'] / 1000)

    aircraft_score = (aircraft['speed'] / 2000 + aircraft['fuel_capacity'] / 5000) / 2

    pilot_skill_score = pilot['skill_level'] / 10

    weather_score = target['weather_score'] / 100

    execution_time_score = mission.get('execution_time_score', 0.5)

    total_score = (
            distance_score * weights['distance'] +
            aircraft_score * weights['aircraft'] +
            pilot_skill_score * weights['pilot_skill'] +
            weather_score * weights['weather'] +
            execution_time_score * weights['execution_time']
    )

    return total_score


def rank_missions(missions: List[Dict[str, Dict]]) -> List[Dict[str, Dict]]:
    return pipe(
        missions,
        partial(sorted, key=calculate_mission_score, reverse=True),
        partial(unique, key=lambda m: m['target']['city']),
        list
    )


def filter_top_missions(missions: List[Dict[str, Dict]], top_n: int = 7) -> List[Dict[str, Dict]]:
    return missions[:top_n]


def get_recommended_missions(missions: List[Dict[str, Dict]], top_n: int = 7) -> List[Dict[str, Dict]]:
    return pipe(
        missions,
        rank_missions,
        partial(filter_top_missions, top_n=top_n)
    )



t = Target('Beirut', 5)
b = get_distance_per_target(t)
print(b)
