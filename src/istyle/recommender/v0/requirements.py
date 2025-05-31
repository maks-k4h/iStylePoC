from typing import NamedTuple
from enum import Enum

class Genders(Enum):
    MALE = 'Male'
    FEMALE = 'Female'


class OutfitRequirementsV0(NamedTuple):
    gender: Genders | None
    temperature_celsius: int | None
    weather_description: str | None
    user_comment: str | None

    @property
    def is_empty(self) -> bool:
        return all(f is None for f in self.__dict__.values())
