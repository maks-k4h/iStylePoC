import gradio as gr


class WelcomeTab:
    def __init__(self) -> None:
        self._build()

    def _build(self) -> None:
        self._define_layout()

    def _define_layout(self) -> None:
        with gr.Tab('Welcome') as self.tab:
            gr.Label('Hello!')