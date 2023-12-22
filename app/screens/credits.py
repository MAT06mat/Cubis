from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
import webbrowser

from data import *
from models import *


Builder.load_file("screens/credits.kv")


# ============ CREDITS ============


class CreditLabel(Label, Loop):
    phase = "r"
    i = 255
    reload = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        Texts.bind(current_lang=self.lang_change)
        Window.bind(on_resize=self.on_window_resize)
        self.on_window_resize()
        self.last_event = Clock.schedule_once(self.wait_time, 10.0)
        self.last_event.cancel()
    
    def lang_change(self, *args):
        self.text = Texts.key(31)
    
    def on_window_resize(self, *args):
        if Window.width < dp(500):
            self.font_size = Window.width/18
        else:
            self.font_size = dp(28)
    
    def pre_enter(self):
        self.reload = False
        self.last_event.cancel()
        self.last_event = Clock.schedule_once(self.wait_time, 8.0)
    
    def wait_time(self, *args):
        self.reload = True
        Settings.easter_egg = True
        Clock.schedule_interval(self.loop, 1/60)
        self.phase = "w"
    
    def loop(self, *args):
        r, g, b = 0, 0, 0
        self.i -= 2
        if self.i < 0:
            self.i = 255
            if self.phase == "w":
                self.phase = "r"
            elif self.phase == "r":
                self.phase = "g"
            elif self.phase == "g":
                self.phase = "b"
            elif self.phase == "b":
                self.phase = "r"
        if self.phase == "w":
            r = 255
            g = self.i
            b = self.i
        elif self.phase == "r":
            r = self.i
            g = 255 - self.i
        elif self.phase == "g":
            g = self.i
            b = 255 - self.i
        elif self.phase == "b":
            b = self.i
            r = 255 - self.i
        
        self.color = (r/255, g/255, b/255, 1)
        if not self.reload:
            self.color = (1, 1, 1, 1)
        return super().loop(*args)
    
    def on_ref_press(self, ref):
        webbrowser.open('https://mat06mat.github.io/MAT06mat/')
        return super().on_ref_press(ref)
