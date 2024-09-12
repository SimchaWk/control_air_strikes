class Pilot:

    def __init__(self, name: str, skill_level: int):
        self.name: str = name
        self.skill_level: int = skill_level

    def __repr__(self) -> str:
        return f'Pilot Name: {self.name}, Skill Level: {self.skill_level}'
