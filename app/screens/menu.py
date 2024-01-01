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
        self.width = Window.width - dp(50)
        self.height = self.width / 1160 * 343
        if self.height > 0.25 * Window.height:
            self.height = 0.25 * Window.height


class MenuBoxLayout(BoxLayout, Loop):
    def loop(self, *args):
        self.width = Window.width - dp(90)
        self.height = self.width / 1289 * 958
        if self.height > 0.5 * Window.height:
            self.height = 0.5 * Window.height
        if self.width > self.height * 1289 / 958:
            self.width = self.height * 1289 / 958


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