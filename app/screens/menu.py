from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.lang import Builder

from data import *
from models import *
from uix import *

import time


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
        self.source = Texts.image_path("atlas://assets/images/buttons/story_mode")


class IMButton(CustomResizeButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        Texts.bind(current_lang=self.lang_change)

    def lang_change(self, *args):
        self.source = Texts.image_path("atlas://assets/images/buttons/infinite_mode")


class HintLabel(Label):
    pass


class FirstHintLabel(HintLabel):
    pass


class SecondHintLabel(HintLabel):
    pass


class HintBoxLayout(RelativeLayout, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.first_label = FirstHintLabel()
        self.hint_image = Image(source="assets/images/help2.png", size_hint=(None, None))
        self.second_label = SecondHintLabel()
        self.add_widget(self.first_label)
        self.add_widget(self.hint_image)
        self.add_widget(self.second_label)
    
    def loop(self, *args) -> bool:
        # Hint systeme
        if Settings.next_hint_time:
            if Settings.next_hint_time < time.time() and Settings.nb_hint < 3:
                Settings.nb_hint += 1
                if Settings.nb_hint < 3:
                    Settings.next_hint_time += 3600
                else:
                    Settings.next_hint_time = None
        else:
            if Settings.nb_hint < 3:
                Settings.next_hint_time = time.time() + 3600
        
        if Settings.nb_hint < 0:
            Settings.nb_hint = 0
        
        # Define text
        self.first_label.text = f"{Settings.nb_hint}"
        if Settings.nb_hint >= 3:
            self.second_label.text = ""
        else:
            next_time = int(Settings.next_hint_time - time.time())
            m = str(next_time//60)
            if len(m) == 1:
                m = "0" + m
            s = str(next_time%60)
            if len(s) == 1:
                s = "0" + s
            self.second_label.text = f"{Texts.key(51)} {m}:{s}"
        
        # Define sizes
        size = self.width / 6
        self.first_label.font_size = size
        self.first_label.center_y = self.center_y
        self.hint_image.size = (size, size)
        self.hint_image.center_y = self.center_y + 2
        self.second_label.font_size = self.width / 8
        self.second_label.center_y = self.center_y
        
        # Define pos
        if Settings.nb_hint >= 3:
            self.hint_image.x = self.width - self.hint_image.width - dp(5)
        else:
            self.second_label.x = self.width - self.second_label.width - dp(10)
            self.hint_image.x = self.second_label.x - self.hint_image.width * 1.1
        self.first_label.x = self.hint_image.x - self.first_label.width
        return super().loop(*args)