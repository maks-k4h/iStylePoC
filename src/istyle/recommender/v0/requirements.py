from typing import NamedTuple
from enum import Enum

class OutfitRequirementsV0(NamedTuple):
    temperature_celsius: int | None
    weather_description: str | None
    user_comment: str | None

    @property
    def is_empty(self) -> bool:
        return all(f is None for f in self.__dict__.values())
