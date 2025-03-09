from pathlib import Path

import gradio as gr

import tabs
from core import wardrobe
from local_storage.storage import LocalWardrobeStorage

wardrobe_storage = LocalWardrobeStorage(Path('/tmp/istyle/wardrobe'), wardrobe.Wardrobe())
if wardrobe_storage.path.exists():
    wardrobe_storage.load()


with gr.Blocks() as demo:
    welcome_tab = tabs.WelcomeTab()
    wardrobe_tab = tabs.WardrobeTab(wardrobe_storage)
    add_item_tab = tabs.AddItemTab(wardrobe_storage)

demo.launch()
