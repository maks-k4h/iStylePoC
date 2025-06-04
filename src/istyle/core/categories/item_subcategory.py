from .item_category import ItemCategory, PredefinedItemCategories


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


class PredefinedItemSubcategories:
    # Tops
    T_SHIRTS = ItemSubcategory(PredefinedItemCategories.TOPS, 'T-Shirts')
    SHIRTS = ItemSubcategory(PredefinedItemCategories.TOPS, 'Shirts')
    # BLOUSES = ItemSubcategory(PredefinedItemCategories.TOPS, 'Blouses')
    SWEATERS = ItemSubcategory(PredefinedItemCategories.TOPS, 'Sweaters')
    HOODIES = ItemSubcategory(PredefinedItemCategories.TOPS, 'Hoodies')
    TANK_TOPS = ItemSubcategory(PredefinedItemCategories.TOPS, 'Tank Tops')

    # Bottoms
    JEANS = ItemSubcategory(PredefinedItemCategories.BOTTOMS, 'Jeans')
    TROUSERS = ItemSubcategory(PredefinedItemCategories.BOTTOMS, 'Trousers')
    SHORTS = ItemSubcategory(PredefinedItemCategories.BOTTOMS, 'Shorts')
    # SKIRTS = ItemSubcategory(PredefinedItemCategories.BOTTOMS, 'Skirts')
    # LEGGINGS = ItemSubcategory(PredefinedItemCategories.BOTTOMS, 'Leggings')
    JOGGERS = ItemSubcategory(PredefinedItemCategories.BOTTOMS, 'Joggers')

    # # One-Piece
    # DRESSES = ItemSubcategory(PredefinedItemCategories.ONE_PIECE, 'Dresses')
    # JUMPSUITS = ItemSubcategory(PredefinedItemCategories.ONE_PIECE, 'Jumpsuits')
    # OVERALLS = ItemSubcategory(PredefinedItemCategories.ONE_PIECE, 'Overalls')
    # ROMPERS = ItemSubcategory(PredefinedItemCategories.ONE_PIECE, 'Rompers')

    # Footwear
    SNEAKERS = ItemSubcategory(PredefinedItemCategories.FOOTWEAR, 'Sneakers')
    BOOTS = ItemSubcategory(PredefinedItemCategories.FOOTWEAR, 'Boots')
    LOAFERS = ItemSubcategory(PredefinedItemCategories.FOOTWEAR, 'Loafers')
    SANDALS = ItemSubcategory(PredefinedItemCategories.FOOTWEAR, 'Sandals')
    # HEELS = ItemSubcategory(PredefinedItemCategories.FOOTWEAR, 'Heels')
    # FLATS = ItemSubcategory(PredefinedItemCategories.FOOTWEAR, 'Flats')

    # Accessories
    BAGS = ItemSubcategory(PredefinedItemCategories.ACCESSORIES, 'Bags')
    HATS = ItemSubcategory(PredefinedItemCategories.ACCESSORIES, 'Hats')
    SCARVES = ItemSubcategory(PredefinedItemCategories.ACCESSORIES, 'Scarves')
    GLOVES = ItemSubcategory(PredefinedItemCategories.ACCESSORIES, 'Gloves')
    BELTS = ItemSubcategory(PredefinedItemCategories.ACCESSORIES, 'Belts')
    SUNGLASSES = ItemSubcategory(PredefinedItemCategories.ACCESSORIES, 'Sunglasses')
    WATCHES = ItemSubcategory(PredefinedItemCategories.ACCESSORIES, 'Watches')

    # Outerwear
    JACKETS = ItemSubcategory(PredefinedItemCategories.OUTERWEAR, 'Jackets')
    COATS = ItemSubcategory(PredefinedItemCategories.OUTERWEAR, 'Coats')
    BLAZERS = ItemSubcategory(PredefinedItemCategories.OUTERWEAR, 'Blazers')
    CARDIGANS = ItemSubcategory(PredefinedItemCategories.OUTERWEAR, 'Cardigans')

    @classmethod
    def list_subcategories(cls) -> list[ItemSubcategory]:
        return [
            value for value in cls.__dict__.values()
            if isinstance(value, ItemSubcategory)
        ]