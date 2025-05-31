from core import item, categories
from item_processing.description.ollama import OllamaItemDescriptor
from local_storage.storage import LocalWardrobeStorage

import gradio as gr


class AddItemTab:
    def __init__(self, s: LocalWardrobeStorage) -> None:
        self._storage = s
        self._build()
        self._item_descriptor = OllamaItemDescriptor()

    def _build(self) -> None:
        self._define_layout()
        self._define_functionality()

    def _define_layout(self) -> None:
        # TAB - Add Item
        with gr.Tab('Add Item'):
            # Layout
            with gr.Row():
                self.item_image = self._get_item_image()
                with gr.Column():
                    self.item_name = self._get_item_name_field()
                    self.item_description = self._get_item_description_field()
                    self.item_seasons = self._get_item_seasons_field()
                    self.item_category_selector = self._get_item_category_selector()
                    self.item_subcategory_selector = self._get_item_subcategory_selector()

            self.add_item_button = self._get_add_item_button()

    def _get_item_image(self):
        return gr.Image(format='png', type='pil', image_mode='RGBA')

    def _get_item_name_field(self, interactive=False, value=None):
        return gr.Textbox(label='Item Name', interactive=interactive, value=value)

    def _get_item_description_field(self, interactive=False, value=None):
        return gr.TextArea(label='Description', interactive=interactive, value=value)

    def _get_item_seasons_field(self, interactive=False, value=[]):
        return gr.Dropdown(
            label='Seasons', choices=[s.value for s in categories.season.Season],
            multiselect=True, interactive=interactive, value=value
        )

    def _get_item_category_selector(self, interactive=False, value=None):
        choices = [
            c.name for c in categories.item_category.PredefinedItemCategories.list_categories()
        ]
        return  gr.Dropdown(label='Category', choices=choices, interactive=interactive, value=value)

    def _get_item_subcategory_selector(self, interactive=False, choices=[], value=None):
        return gr.Dropdown(label='Subcategory', choices=choices, interactive=interactive, value=value)

    def _get_add_item_button(self, value=None):
        return gr.Button('Add Item!', value=value)

    def _define_functionality(self) -> None:
        # Functionality
        def on_image_uploaded(image):
            gr.Info('Analyzing item...')
            res = self._item_descriptor.describe_by_image(image)
            gr.Success('Item analyzed!')
            return [
                self._get_item_name_field(True, res.name),
                self._get_item_description_field(True, res.description),
                self._get_item_seasons_field(True, [v.value for v in res.seasons]),
                self._get_item_category_selector(True, res.category.name),
                self._get_item_subcategory_selector(True, [
                    sc.name for sc in categories.item_subcategory.PredefinedItemSubcategories.list_subcategories()
                    if sc.category.name == res.category.name
                ], res.subcategory.name),
            ]

        self.item_image.upload(on_image_uploaded, inputs=[self.item_image], outputs=[
            self.item_name, self.item_description,
            self.item_seasons, self.item_category_selector,
            self.item_subcategory_selector
        ])

        self.item_category_selector.select(lambda cat_name: self._get_item_subcategory_selector(True, choices=[
            sc.name for sc in categories.item_subcategory.PredefinedItemSubcategories.list_subcategories()
            if sc.category.name == cat_name
        ]), inputs=[self.item_category_selector], outputs=[self.item_subcategory_selector])

        def add_item(image, name, description, seasons, subcategory_name):
            if not image:
                raise gr.Error('Provide item image!')
            if not name:
                raise gr.Error('Provide item name!')
            if not seasons or len(seasons) == 0:
                raise gr.Error('Provide item seasons!')
            if not subcategory_name:
                raise gr.Error('Select category and subcategory!')

            item_obj = item.WardrobeItem(
                name=name,
                description=description,
                seasons=[categories.season.Season(s) for s in seasons],
                image=image,
                subcategory=[c for c in categories.item_subcategory.PredefinedItemSubcategories.list_subcategories()
                             if c.name == subcategory_name][0]
            )
            self._storage.wardrobe.add_item(item_obj)
            self._storage.store()
            gr.Success(f'Item {name} successfully added.')

        self.add_item_button.click(add_item, inputs=[
                self.item_image, self.item_name, self.item_description, self.item_seasons, self.item_subcategory_selector
        ])