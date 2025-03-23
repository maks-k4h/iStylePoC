import json

from PIL import Image

import torch
from transformers import Qwen2_5_VLForConditionalGeneration, Qwen2_5_VLProcessor

from core import item, categories
from . import abstract


PROMPT_A = '''
You are given a photo of an outfit item. Analyze the image and provide a structured JSON response with the following properties:
 - name: A concise and accurate name of the item (e.g., "Blue denim jacket", "Black wool sweater").
 - description: A detailed yet concise description of the item, highlighting key features such as material, color, patterns, or other characteristics that can help match it with outfits.
 - seasons: An array indicating the suitable seasons for wearing this item. The seasons must be from {seasons}.

Output Format:
Your response must strictly adhere to the following JSON format without deviation:

{{
  "name": "name of the item here",
  "description": "detailed description here",
  "seasons": ["Season A", "Season B"]
}}

Ensure your response is a valid JSON object, free of formatting errors or additional text.
'''.format(seasons=", ".join([f'"{s.value}"' for s in categories.season.Season]))

# _SUBCATEGORIES_TEXT = '\n'.join(f'{c.name}:\n' + ''.join(f' - {sc.name}\n' for sc in categories.item_subcategory.PredefinedItemSubcategories.list_subcategories()
#                                                   if sc.category.name == c.name)
#                                 for c in categories.item_category.PredefinedItemCategories.list_categories())
_SUBCATEGORIES_TEXT = ''.join(f' - {sc.name}\n' for sc in categories.item_subcategory.PredefinedItemSubcategories.list_subcategories())
PROMPT_B = f'''
You are given the name, description, and suitable seasons of an outfit item. Your task is to classify the item into the most appropriate item category based on the predefined list.
Here are available item types:
{_SUBCATEGORIES_TEXT} ''' + '''

Input:
- **name**: {name}
- **description**: {description}
- **seasons**: {seasons}

Output Format:
Your response must strictly adhere to the following JSON format without deviation:

{{
  "item_type": "Most relevant item category"
}}

Ensure your response is a valid JSON object, free of formatting errors or additional text. Only choose item type from the list of categories provided.
'''


class Qwen25VLItemDescriptor(abstract.AbstractItemDescriptor):
    def __init__(self) -> None:
        self._model = None
        self._processor = None
        self._target_pixels = 256 * 256

    def _check_model(self) -> None:
        if self._model is not None and self._processor is not None:
            return
        CHECKPOINT = 'Qwen/Qwen2.5-VL-3B-Instruct'
        self._model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            CHECKPOINT, torch_dtype=torch.bfloat16,  # device_map='mps'
        )
        self._processor = Qwen2_5_VLProcessor.from_pretrained(
            CHECKPOINT
        )

    def describe_by_image(self, item_image: Image.Image) -> item.WardrobeItem:
        self._check_model()  # lazy load

        item_image = self._preprocess_image(item_image)
        print(f'New image size: {item_image.size}')

        # Get 'name', 'description', 'seasons'
        def get_NDS():
            messages = [
                {
                    'role': 'system',
                    'content': [
                        {'type': 'image', 'image': item_image},
                        {'type': 'text', 'text': PROMPT_A}
                    ]
                }
            ]
            text = self._processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = self._processor(text=[text], images=[item_image], return_tensors='pt')
            gen_ids = self._model.generate(**inputs.to(self._model.device), max_new_tokens=256)
            gen_ids = [
                out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, gen_ids)
            ]
            response_text = self._processor.batch_decode(gen_ids, skip_special_tokens=True)[0]
            print(response_text)
            response_data = json.loads(self._try_strip_json(response_text))
            return (
                response_data.get('name', 'Default Name'),
                response_data.get('description', 'Default Description'),
                [categories.season.Season(s[0].upper() + s[1:].lower()) for s in response_data.get('seasons', [])]
            )
        name, description, seasons = get_NDS()

        # Get 'category' and 'subcategory'
        def get_subcategory():
            messages = [
                {
                    'role': 'system',
                    'content': [
                        {'type': 'text', 'text': PROMPT_B.format(
                            name=name, description=description,
                            seasons=', '.join(s.value for s in seasons)
                        )},
                    ]
                }
            ]
            text = self._processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = self._processor(text=[text], return_tensors='pt')
            gen_ids = self._model.generate(**inputs.to(self._model.device), max_new_tokens=128)
            gen_ids = [
                out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, gen_ids)
            ]
            response_text = self._processor.batch_decode(gen_ids, skip_special_tokens=True)[0]
            print(response_text)
            response_data = json.loads(self._try_strip_json(response_text))
            subcategory_text = response_data.get(
                'item_type',
                'default'
            )
            candidates = [sc for sc in categories.item_subcategory.PredefinedItemSubcategories.list_subcategories()
                          if sc.name.lower() == subcategory_text.lower()]
            return candidates[0] if len(candidates) > 0 else categories.item_subcategory.PredefinedItemSubcategories.T_SHIRTS

        subcategory = get_subcategory()

        return item.WardrobeItem(
            name=name,
            description=description,
            image=item_image,
            seasons=seasons,
            subcategory=subcategory,
        )

    def _preprocess_image(self, im: Image) -> Image.Image:
        width, height = im.size
        aspect_ratio = width / height

        # Start with an initial guess
        new_width = int((self._target_pixels * aspect_ratio) ** 0.5)
        new_height = int(new_width / aspect_ratio)

        # Adjust to ensure the total number of pixels is not more than the target
        while new_width * new_height > self._target_pixels:
            new_width -= 1
            new_height = int(new_width / aspect_ratio)

        return im.resize((new_width, new_height))

    def _try_strip_json(self, s: str) -> str:
        start = s.find('{')
        end = s.rfind('}')

        if start == -1 or end == -1 or start > end:
            return s
        return s[start:end + 1]
