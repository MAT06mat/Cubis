from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.lang import Builder

Builder.load_file("src/base.kv")

class Loop:
    def __init__(self) -> None:
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        pass


class Cadre(Image):
    pass


class MyBackgroundImage(FloatLayout):
    pass