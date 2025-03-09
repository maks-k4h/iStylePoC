import gradio as gr

from PIL import Image
from core import item, categories
from local_storage.storage import LocalWardrobeStorage


class WardrobeTab:
    def __init__(self, s: LocalWardrobeStorage) -> None:
        self._storage = s
        self._build()

    def _build(self) -> None:
        self._define_layout()
        self._define_functionality()

    def _define_layout(self) -> None:
        with gr.Tab('Wardrobe') as self.tab:
            self.items_gallery = self._get_items_gallery()
            with gr.Row() as self.current_item_component:
                with gr.Column():
                    self.item_image = self._get_item_image()
                with gr.Column():
                    self.item_name = self._get_item_name()
                    self.item_description = self._get_item_description()
                    self.item_seasons = self._get_item_seasons()
                    self.category_selector = self._get_category_selector()
                    self.subcategory_selector = self._get_subcateogry_selector()
                    self.item_index = self._get_item_index()

            with gr.Row():
                self.save_button = gr.Button("Save Changes")
                self.delete_button = gr.Button("Delete Item")

    def _get_items_gallery(self) -> gr.Gallery:
        return gr.Gallery(
            [(v.image, str(i)) for i, v in enumerate(self._storage.wardrobe.items)],
            columns=5,
            height=500,
            allow_preview=False,
            interactive=False,
        )

    def _get_item_image(self, i: item.WardrobeItem | None = None) -> Image.Image:
        return gr.Image(i.image if i is not None else None, interactive=False)

    def _get_item_name(self, i: item.WardrobeItem | None = None) -> gr.Component:
        return gr.Textbox(label='Name', value='' if i is None else i.name, interactive=True)

    def _get_item_description(self, i: item.WardrobeItem | None = None) -> gr.Component:
        return gr.TextArea(label='Description', value='' if i is None else i.description, interactive=True)

    def _get_item_seasons(self, i: item.WardrobeItem | None = None) -> gr.Component:
        return gr.Dropdown(label="Seasons",
                           choices=[s.value for s in categories.season.Season],
                           value=None if i is None else [s.value for s in i.seasons],
                           multiselect=True, interactive=True)

    def _get_category_selector(self, i:item.WardrobeItem | None = None) -> gr.Component:
        return gr.Dropdown(label="Category",
                           choices=[c.name for c in categories.item_category.PredefinedItemCategories.list_categories()],
                           value=i.category.name if i is not None else None,
                           interactive=True)

    def _get_subcateogry_selector(self, i:item.WardrobeItem | None = None) -> gr.Component:
        return gr.Dropdown(label="Subcategory",
                           choices=[sc.name for sc in categories.item_subcategory.PredefinedItemSubcategories.list_subcategories()],
                           value=None if i is None else i.subcategory.name,
                           interactive=True)

    def _get_item_index(self, item_index: int | None = None) -> gr.Component:
        return gr.Number(value=item_index, visible=False)

    def _define_functionality(self) -> None:
        self.tab.select(lambda: self._get_items_gallery(), outputs=[self.items_gallery])

        def select_item(value, evt: gr.EventData) -> list:
            item_index = evt._data['index']
            selected_item = self._storage.wardrobe.items[item_index]
            return [
                self._get_item_image(selected_item),
                self._get_item_name(selected_item),
                self._get_item_description(selected_item),
                self._get_item_seasons(selected_item),
                self._get_category_selector(selected_item),
                self._get_subcateogry_selector(selected_item),
                self._get_item_index(item_index)
            ]

        self.items_gallery.select(select_item,
                                  inputs=[self.items_gallery],
                                  outputs=[self.item_image, self.item_name, self.item_description, self.item_seasons, self.category_selector, self.subcategory_selector, self.item_index])

        def save_changes(i, name, description, seasons, item_category, item_subcategory) -> None:
            current_item = self._storage.wardrobe.items[i]
            current_item.name = name
            current_item.description = description
            current_item.seasons = [categories.season.Season(s) for s in seasons]
            current_item.subcategory = categories.item_subcategory.ItemSubcategory(categories.item_category.ItemCategory(item_category), item_subcategory)
            gr.Info('Item Updated!')

        self.save_button.click(save_changes,
                               inputs=[self.item_index, self.item_name, self.item_description, self.item_seasons, self.category_selector, self.subcategory_selector], outputs=[])

        def delete_item(i) -> list:
            del self._storage.wardrobe[i]
            self._storage.store()
            gr.Info('Item Deleted!')
            return [
                self._get_items_gallery(),
                self._get_item_image(),
                self._get_item_name(),
                self._get_item_description(),
                self._get_item_seasons(),
                self._get_category_selector(),
                self._get_subcateogry_selector()
            ]

        self.delete_button.click(delete_item, inputs=[self.item_index],
                                 outputs=[self.items_gallery, self.item_image, self.item_name, self.item_description, self.item_seasons, self.category_selector, self.subcategory_selector])

