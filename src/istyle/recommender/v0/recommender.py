import random

from pydantic import BaseModel, Field

import ollama


from . import requirements
from core import wardrobe, item


class OutfitRecommenderV0:
    def __init__(self, w: wardrobe.Wardrobe):
        self._wardrobe = w
        self._model = 'gemma3:4b'

        self._client = ollama.Client(
            host='http://localhost:11434'
        )

    def recommend(self, r: requirements.OutfitRequirementsV0) -> list[list[item.WardrobeItem]]:
        shuffled_items = self._wardrobe.items.copy()
        random.shuffle(shuffled_items)
        messages = [
            {
                'role': 'system',
                'content': 'You are a professional outfit advisor'
            },
            {
                'role': 'user',
                'content': (
                    "Create the perfect outfit using ONLY items from the user's wardrobe below. "
                    "Your recommendation must be weather-appropriate and address all user requirements.\n\n"

                    "### Wardrobe Constraints:\n"
                    "- ONLY use items from this list\n"
                    "- ENSURE to include footwear\n"
                    "- NEVER reference non-existent items\n"
                    "- **Each outfit must be complete(!)** (covers all body needs for the weather)\n\n"

                    "## Wardrobe Inventory\n" +
                    '\n'.join(
                        f'### {cat} \n' +
                        '\n'.join(f' - {itm.name} ({idx+1}) {itm.description}' for idx, itm in enumerate(shuffled_items) if itm.category.name == cat)
                        for cat in {i.category.name for i in shuffled_items}
                    ) + '\n\n'

                    "## User Requirements\n"
                    f"- Temperature: {r.temperature_celsius}°C\n"
                    f"- Weather: {r.weather_description}\n"
                    f"- Special Requests: '{r.user_comment}'\n\n"

                    "## Output Instructions\n"
                    "1. **Reasoning** (100-200 words):\n"
                    "   - Analyze temperature, weather, and personal preferences impact\n"
                    "   - Figure out outfit layers \n"
                    "   - Justify item choices USING ITEM NAMES FOLLOWED BY ITEM IDENTIFIERS \n"

                    "2. **Item Identifiers**:\n"
                    "   - MUST correspond to wardrobe items\n"
                    "   - Include ALL essential layers (base/mid/outer)\n\n"

                    "## Critical Rules\n"
                    "- REJECT items incompatible with current temperature/weather\n"
                    "- If user requests 'formal', avoid casual items\n"
                    "- **Missing layer / footwear = incomplete outfit**\n"
                    f"- Item numbers MUST EXIST in wardrobe (1-{len(self._wardrobe.items)})\n"
                )
            }
        ]

        class OutfitRecommendation(BaseModel):
            reasoning: str = Field(
                description="Step-by-step justification using item numbers. 100-200 words",
            )
            item_names: list[str] = Field(
                description="Names of the items in the outfit"
            )
            item_identifiers: list[int] = Field(
                description=f"Exact item IDs from wardrobe (1-{len(self._wardrobe.items)})",
            )

        print(messages[1]['content'])

        response = self._client.chat(
            model=self._model,
            messages=messages,
            format=OutfitRecommendation.model_json_schema(),
            options={'temperature': 0.0},
            think=False,
        )

        print(response.message.content)

        recommended_outfit = OutfitRecommendation.model_validate_json(response.message.content)

        return [[
            shuffled_items[i - 1] for i in recommended_outfit.item_identifiers
        ]]
