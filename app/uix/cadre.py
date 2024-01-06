from kivy.uix.image import Image


class Cadre(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = "assets/images/elements/frame.png"