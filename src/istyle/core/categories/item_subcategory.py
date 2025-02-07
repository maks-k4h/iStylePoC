from .item_category import ItemCategory


class ItemSubcategory:
    def __init__(self, category: ItemCategory, name: str) -> None:
        self._category = category
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def category(self) -> ItemCategory:
        return self._category
