from abc import ABC, abstractmethod
from PIL import Image

from core import item


class AbstractItemDescriptor(ABC):
    @abstractmethod
    def describe_by_image(self, item_image: Image.Image) -> item.WardrobeItem:
        pass