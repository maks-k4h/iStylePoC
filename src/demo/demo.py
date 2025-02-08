from pathlib import Path

import gradio as gr

from core import categories, wardrobe, item
from core.image.image import Image
from local_storage.storage import LocalWardrobeStorage

wardrobe_storage = LocalWardrobeStorage(Path('/tmp/istyle/wardrobe'), wardrobe.Wardrobe())
if wardrobe_storage.path.exists():
    wardrobe_storage.load()


with gr.Blocks() as demo:
    with gr.Tab('Wardrobe'):
        # Layout
        items_gallery = gr.Gallery(
            value=[i.image.to_numpy() for i in wardrobe_storage.wardrobe.items],
            columns=5,
            height=500,
        )

        # Functionality

    with gr.Tab('Add Item'):
        # Layout
        with gr.Row():
            item_image = gr.Image(format='png', type='filepath', image_mode='RGBA')
            with gr.Column():
                item_name = gr.Textbox(label='Item Name')
                item_description = gr.TextArea(label='Description')
                item_seasons = gr.Dropdown(label='Seasons', choices=[s.value for s in categories.season.Season], multiselect=True)
                category_selector = gr.Dropdown(label='Category', value=None, choices=[
                    c.name for c in categories.item_category.PredefinedItemCategories.list_categories()
                ])
                subcategory_selector = gr.Dropdown(label='Subcategory', choices=[])

        # Functionality

        category_selector.select(lambda cat_name: gr.Dropdown(choices=[
            sc.name for sc in categories.item_subcategory.PredefinedItemSubcategories.list_subcategories()
            if sc.category.name == cat_name
        ]), inputs=[category_selector], outputs=[subcategory_selector])

        subcategory_selector.select(lambda _: print('Hello!'), inputs=[subcategory_selector])

        def add_item(s_image_path, name, description, seasons, subcategory_name) -> None:
            if not s_image_path:
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
                image=Image.from_file(Path(s_image_path)),
                subcategory=[c for c in categories.item_subcategory.PredefinedItemSubcategories.list_subcategories()
                             if c.name == subcategory_name][0]
            )
            wardrobe_storage.wardrobe.add_item(item_obj)
            wardrobe_storage.store()
            gr.Success(f'Item {name} successfully added.')

        gr.Button('Add Item!').click(add_item, inputs=[
            item_image, item_name, item_description, item_seasons, subcategory_selector])

demo.launch()