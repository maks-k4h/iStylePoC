from core import wardrobe, item
from . import requirements


class OutfitRecommenderV0:
    def __init__(self, w: wardrobe.Wardrobe):
        self._wardrobe = w

    def recommend(self, r: requirements.OutfitRequirementsV0) -> list[list[item.WardrobeItem]]:
        ...

