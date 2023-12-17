from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.lang import Builder
from random import randint
import webbrowser

from data.settings import Settings
from data.texts import Texts
from models.loop import Loop


Builder.load_file("screens/credits.kv")


# ============ CREDITS ============


class CreditLabel(Label, Loop):
    r = 255
    g = 255
    b = 255
    reload = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        Texts.bind(current_lang=self.lang_change)
        self.last_event = Clock.schedule_once(self.wait_time, 10.0)
        self.last_event.cancel()
    
    def lang_change(self, *args):
        self.text = Texts.key(31)
    
    def pre_enter(self):
        self.reload = False
        self.last_event.cancel()
        self.last_event = Clock.schedule_once(self.wait_time, 10.0)
    
    def wait_time(self, *args):
        self.reload = True
        Settings.easter_egg = True
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        self.r += randint(-10, 10)
        self.g += randint(-10, 10)
        self.b += randint(-10, 10)
        if self.r > 200:
            self.r = 200
        if self.g > 200:
            self.g = 200
        if self.b > 200:
            self.b = 200
        if self.r < 50:
            self.r = 50
        if self.g < 50:
            self.g = 50
        if self.b < 50:
            self.b = 50
        self.color = (self.r/255, self.g/255, self.b/255, 1)
        if not self.reload:
            self.color = (1, 1, 1, 1)
        return super().loop(*args)
    
    def on_ref_press(self, ref):
        webbrowser.open('https://mat06mat.github.io/matthieufelten/')
        return super().on_ref_press(ref)
