from PIL import Image

from .categories.item_category import ItemCategory
from .categories.season import Season
from .categories.item_subcategory import ItemSubcategory


class WardrobeItem:
    def __init__(
            self,
            name: str,
            description: str,
            image: Image,
            seasons: list[Season],
            subcategory: ItemSubcategory,
    ) -> None:
        self._name = name
        self._description = description
        self._image = image
        self._seasons = seasons
        self._subcategory = subcategory

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        self._description = description

    @property
    def image(self) -> Image:
        return self._image

    @property
    def seasons(self) -> list[Season]:
        return self._seasons

    @seasons.setter
    def seasons(self, seasons: list[Season]) -> None:
        self._seasons = seasons

    @property
    def category(self) -> ItemCategory:
        return self._subcategory.category

    @property
    def subcategory(self) -> ItemSubcategory:
        return self._subcategory

    @subcategory.setter
    def subcategory(self, subcategory: ItemSubcategory) -> None:
        self._subcategory = subcategory
