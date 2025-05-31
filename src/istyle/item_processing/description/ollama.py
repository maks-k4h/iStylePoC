import io
import json
import tempfile

from PIL import Image

import ollama

from core import item, categories
from . import abstract


PROMPT_A = '''
You are given a photo of an outfit item. Analyze the image and provide a structured JSON response with the following properties:
 - description: A detailed yet concise description of the item, highlighting key features such as material, color, patterns, or other characteristics that can help match it with outfits.
 - name: A concise and accurate name of the item (for example, "Blue denim jacket", "Black wool sweater", "White cargo pants", etc.).
 - seasons: An array indicating the suitable seasons for wearing this item. The seasons must be from {seasons}.

Output Format:
Your response must strictly adhere to the following JSON format without deviation:

{{
  "name": "name of the item here",
  "description": "detailed description here. Must be 100-150 words",
  "seasons": ["Season A", "Season B"]
}}

Ensure your response is a valid JSON object, free of formatting errors or additional text.
'''.format(seasons=", ".join([f'"{s.value}"' for s in categories.season.Season]))

# _SUBCATEGORIES_TEXT = '\n'.join(f'{c.name}:\n' + ''.join(f' - {sc.name}\n' for sc in categories.item_subcategory.PredefinedItemSubcategories.list_subcategories()
#                                                   if sc.category.name == c.name)
#                                 for c in categories.item_category.PredefinedItemCategories.list_categories())
_SUBCATEGORIES_TEXT = ''.join(f' - {sc.name}\n' for sc in categories.item_subcategory.PredefinedItemSubcategories.list_subcategories())
PROMPT_B = f'''
Your task is to classify this item into the most appropriate item category based on the predefined list.
Here are available categories:
{_SUBCATEGORIES_TEXT} ''' + '''

Output Format:
Your response must strictly adhere to the following JSON format without deviation:

{{
  "category": "Most relevant item category"
}}

Ensure your response is a valid JSON object, free of formatting errors or additional text. Only choose item category from the list of the categories provided.
'''


class OllamaItemDescriptor(abstract.AbstractItemDescriptor):
    def __init__(self) -> None:
        self._model = 'qwen2.5vl:3b'
        self._client = ollama.Client(
            host='http://localhost:11434'
        )

    def describe_by_image(self, item_image: Image.Image) -> item.WardrobeItem:
        path_item_image = (
            lambda f: (self._resize_if_needed(item_image, 512).save(f), f)[1]
        )(tempfile.NamedTemporaryFile(suffix=".png", delete=False).name)
        # print(path_item_image)

        messages = [
            {
                'role': 'user',
                'content': PROMPT_A,
                'images': [path_item_image],
            }
        ]

        response = self._client.chat(
            model=self._model,
            messages=messages,
            options={
                'temperature': 0
            }
        )

        response_data = json.loads(self._try_strip_json(response.message.content))

        name, description, seasons = (
            response_data.get('name', 'Default Name'),
            response_data.get('description', 'Default Description'),
            [categories.season.Season(s[0].upper() + s[1:].lower()) for s in response_data.get('seasons', [])]
        )

        messages.append({
            'role': response.message.role,
            'content': response.message.content,
        })

        messages.append({
            'role': 'user',
            'content':  PROMPT_B
        })

        response = self._client.chat(
            model=self._model,
            messages=messages,
            options={
                'temperature': 0
            }
        )

        response_data = json.loads(self._try_strip_json(response.message.content))
        subcategory_text = response_data.get(
            'category',
            'default'
        )
        candidates = [sc for sc in categories.item_subcategory.PredefinedItemSubcategories.list_subcategories()
                      if sc.name.lower() == subcategory_text.lower()]
        subcategory = candidates[0] if len(candidates) > 0 else categories.item_subcategory.PredefinedItemSubcategories.T_SHIRTS

        return item.WardrobeItem(
            name=name,
            description=description,
            image=item_image,
            seasons=seasons,
            subcategory=subcategory,
        )

    def _try_strip_json(self, s: str) -> str:
        start = s.find('{')
        end = s.rfind('}')

        if start == -1 or end == -1 or start > end:
            return s
        return s[start:end + 1]

    @staticmethod
    def _resize_if_needed(im, max_side):
        return im if max(im.size) <= max_side else im.resize(tuple(int(max_side * s / max(im.size)) for s in im.size), Image.LANCZOS)
