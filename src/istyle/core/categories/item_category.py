
class ItemCategory:
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self) -> str:
        return self._name


class PredefinedItemCategories:
    TOPS = ItemCategory('Tops')
    BOTTOMS = ItemCategory('Bottoms')
    # ONE_PIECE = ItemCategory('One-Piece')
    OUTERWEAR = ItemCategory('Outerwear')
    FOOTWEAR = ItemCategory('Footwear')
    ACCESSORIES = ItemCategory('Accessories')

    @classmethod
    def list_categories(cls) -> list[ItemCategory]:
        return [
            value for value in cls.__dict__.values()
            if isinstance(value, ItemCategory)
        ]
