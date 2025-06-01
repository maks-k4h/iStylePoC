from cProfile import label

import gradio as gr
from PIL import Image
from torch.utils.hipify.hipify_python import value

import recommender
from core import item, categories
from local_storage.storage import LocalWardrobeStorage


class RecommendationsTab:
    def __init__(self, s: LocalWardrobeStorage) -> None:
        self._storage = s
        self._recommender = recommender.v0.OutfitRecommenderV0(self._storage.wardrobe)
        self._build()

    def _build(self) -> None:
        self._define_layout()
        self._define_functionality()

    def _define_layout(self) -> None:
        with gr.Tab('Recommendations') as tab:
            with gr.Row():
                with gr.Column():
                    self._temperature_input = self._get_temperature_input()
                    self._weather_input = self._get_weather_input()
                    self._user_comment_input = self._get_user_comment_input()
                    self._recommend_button = self._get_recommend_button()

                with gr.Column():
                    self._outfit_gallery = self._get_outfit_gallery()

    def _get_temperature_input(self):
        return gr.Slider(minimum=-20, maximum=40, step=1, value=15)

    def _get_weather_input(self):
        return gr.Textbox(label='Weather conditions')

    def _get_user_comment_input(self):
        return gr.Textbox(label='User comment')

    def _get_recommend_button(self):
        return gr.Button("Recommend!")

    def _get_outfit_gallery(self, outfit: list[item.WardrobeItem] | None = None):
        return gr.Gallery(
            None if outfit is None else [i.image for i in outfit],
            allow_preview=False,
            interactive=False,
        )

    def _define_functionality(self) -> None:
        def on_recommend(temperature, weather, user_comment):
            requirements = recommender.v0.requirements.OutfitRequirementsV0(
                temperature_celsius=temperature,
                weather_description=weather,
                user_comment=user_comment,
            )
            outfit = self._recommender.recommend(requirements)[0]
            return self._get_outfit_gallery(outfit)
        self._recommend_button.click(on_recommend, inputs=[
            self._temperature_input,
            self._weather_input, self._user_comment_input
        ], outputs=[self._outfit_gallery])
