class Target:

    def __init__(self, city: str, priority: int, weather_score: float = 0, distance: float = 0):
        self.city: str = city
        self.priority: int = priority
        self.weather_score: float = weather_score
        self.distance: float = distance

    def __repr__(self) -> str:
        return f'Target: {self.city}, Priority: {self.priority}'
