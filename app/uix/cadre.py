from kivy.uix.image import Image


class Cadre(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = "atlas://assets/images/elements/frame"