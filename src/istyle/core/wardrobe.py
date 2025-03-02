from . import item
from .categories import item_category, item_subcategory


class Wardrobe:
    def __init__(
            self,
            items: list[item.WardrobeItem] | None = None
    ) -> None:
        self._items = items if items is not None else []

    @property
    def items(self) -> list[item.WardrobeItem]:
        return self._items

    def add_item(self, i: item.WardrobeItem) -> None:
        self._items.append(i)

    def __delitem__(self, key) -> None:
        del self._items[key]

    def items_by_category(self, category: item_category.ItemCategory) -> list[item.WardrobeItem]:
        return [i for i in self.items if i.subcategory.category.name == category.name]

    def items_by_subcategory(self, subcategory: item_subcategory.ItemSubcategory) -> list[item.WardrobeItem]:
        return [i for i in self.items if i.subcategory.name == subcategory.name]

    def clean(self) -> None:
        self._items = []
