import argparse
import sys

from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent.parent / 'istyle'))

from core.wardrobe import Wardrobe
from local_storage.storage import LocalWardrobeStorage
from item_processing.description.ollama import OllamaItemDescriptor


def main(
        p_images: Path,
        p_wardrobe: Path,
) -> None:
    descriptor = OllamaItemDescriptor()
    wardrobe = LocalWardrobeStorage(p_wardrobe, Wardrobe())
    wardrobe.load()
    for image in p_images.iterdir():
        if image.suffix not in ['.jpg', '.png', '.jpeg', '.webp']:
            continue
        print('Processing', image.name)
        item = descriptor.describe_by_image(Image.open(image))
        wardrobe.wardrobe.add_item(item)
        wardrobe.store()

    print('Done!')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=(
        "This utility automates the process of adding new items to a wardrobe. "
        "Specifically, it takes a set of images, processes them with AI (description) "
        "and adds them to the wardrobe."
    ))

    parser.add_argument('images', type=Path, )
    parser.add_argument('wardrobe', type=Path)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args.images, args.wardrobe)