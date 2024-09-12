class Aircraft:

    def __init__(self, ac_type: str, speed: float, fuel_capacity: float):
        self.type: str = ac_type
        self.speed: float = speed
        self.fuel_capacity: float = fuel_capacity

    def __repr__(self) -> str:
        return f'Aircraft Type: {self.type}, speed: {self.speed}, fuel capacity: {self.fuel_capacity}'
