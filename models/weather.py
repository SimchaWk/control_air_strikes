class Weather:

    def __init__(self, temperature: float, wind_speed: float, precipitation: float, cloud_cover: float):
        self.temperature: float = temperature
        self.wind_speed: float = wind_speed
        self.precipitation: float = precipitation
        self.cloud_cover: float = cloud_cover

    def __repr__(self) -> str:
        return (f'Weather: Temperature: {self.temperature}°C, Wind Speed: {self.wind_speed} m/s,'
                f' Precipitation: {self.precipitation} mm, Cloud Cover: {self.cloud_cover}%')
