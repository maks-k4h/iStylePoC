import json
from pathlib import Path

from PIL import Image

from core import wardrobe, item, categories
from core.wardrobe import Wardrobe


class LocalWardrobeStorage:
    """
    Instances of this class connect Wardrobe instances with filesystem.
    Wardrobe can be loaded or stored.

    Storage directory structure:

    - storage_dir_name
      | - category_subcategory_id.json
      | - category_subcategory_id.png
      ...
    """


    def __init__(
            self,
            p_storage: Path,
            wardrobe_to_track: wardrobe.Wardrobe
    ) -> None:
        """
        Uses .load() to load wardrobe from p_storage.
        :param p_storage:
        """
        self._p = p_storage
        self._w = wardrobe_to_track

    @property
    def path(self) -> Path:
        return self._p

    @property
    def wardrobe(self) -> Wardrobe:
        return self._w

    def load(self) -> None:
        """
        Load wardrobe from the filesystem.
        :return:
        """
        self._w.clean()
        item_identifiers = [p.stem for p in sorted(self._p.iterdir()) if p.suffix == ".json"]

        for item_i in item_identifiers:
            p_image = self._p / (item_i + ".png")
            image = Image.open(p_image)

            p_json = self._p / (item_i + ".json")
            meta = json.loads(p_json.read_text())
            name = meta["name"]
            description = meta["description"]
            seasons = [categories.season.Season(s) for s in meta["seasons"]]
            category = categories.item_category.ItemCategory(meta["category"])
            subcategory = categories.item_subcategory.ItemSubcategory(category, meta["subcategory"])

            item_obj = item.WardrobeItem(
                name=name,
                description=description,
                image=image,
                seasons=seasons,
                subcategory=subcategory,
            )
            self._w.add_item(item_obj)

    def store(self) -> None:
        """
        Export wardrobe's data to the filesystem.
        :return: None
        """
        self._p.mkdir(exist_ok=True, parents=True)
        for i, item_obj in enumerate(self._w.items):
            item_identifier = (f'{item_obj.category.name}_{item_obj.subcategory.name}_{i}'
                               .replace(' ', '-').lower())
            p_image = self._p / (item_identifier + ".png")
            item_obj.image.save(p_image)

            p_json = self._p / (item_identifier + ".json")
            meta = {
                'name': item_obj.name,
                'description': item_obj.description,
                'seasons': [s.value for s in item_obj.seasons],
                'category': item_obj.category.name,
                'subcategory': item_obj.subcategory.name,
            }
            p_json.write_text(json.dumps(meta, indent=2))
