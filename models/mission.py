from datetime import datetime
from models.aircraft import Aircraft
from models.pilot import Pilot
from models.target import Target
from models.weather import Weather


class Mission:

    def __init__(self, target: 'Target', pilot: 'Pilot', aircraft: 'Aircraft', departure_time: datetime,
                 weather: 'Weather', distance: float):
        self.target: 'Target' = target
        self.pilot: 'Pilot' = pilot
        self.aircraft: 'Aircraft' = aircraft
        self.departure_time: datetime = departure_time
        self.weather: 'Weather' = weather
        self.distance: float = distance

    def __repr__(self) -> str:
        return (f'Mission to {self.target}: Pilot: {self.pilot.name}, Aircraft: {self.aircraft.type}, '
                f'Departure: {self.departure_time}, Distance: {self.distance} km')
