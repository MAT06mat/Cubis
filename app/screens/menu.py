from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.lang import Builder

from data import *
from models import *
from uix import *


Builder.load_file("screens/menu.kv")


# ============ MAIN MENU ============


class Logo(Image, Loop):   
    def loop(self, *args):
        self.width = Window.width - dp(30)
        self.height = self.width / 1160 * 343
        while self.height > 0.3 * Window.height:
            self.height -= 1


class MenuBoxLayout(BoxLayout, Loop):
    def loop(self, *args):
        self.width = Window.width - dp(50)
        self.height = self.width / 1289 * 958
        while self.height > 0.6 * Window.height:
            self.height -= 1
        while self.width / 1289 * 958 > self.height:
            self.width -= 1


class SMButton(CustomResizeButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        Texts.bind(current_lang=self.lang_change)

    def lang_change(self, *args):
        self.source = Texts.image_path("assets/images/buttons/story_mode.png")


class IMButton(CustomResizeButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        Texts.bind(current_lang=self.lang_change)

    def lang_change(self, *args):
        self.source = Texts.image_path("assets/images/buttons/infinite_mode.png")