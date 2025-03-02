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
        return self._subcategory.name

    @property
    def description(self) -> str:
        return self._description

    @property
    def image(self) -> Image:
        return self._image

    @property
    def seasons(self) -> list[Season]:
        return self._seasons

    @property
    def category(self) -> ItemCategory:
        return self._subcategory.category

    @property
    def subcategory(self) -> ItemSubcategory:
        return self._subcategory
