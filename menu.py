from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from random import randint

from data import SETTINGS


class MusicSlider(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = SETTINGS.get("Music")
    
    def on_value(self, *args):
        SETTINGS.modify("Music", int(self.value))


class EffectSlider(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.value = SETTINGS.get("Effect")
    
    def on_value(self, *args):
        SETTINGS.modify("Effect", int(self.value))


class SettingImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.loop, 1/60)
        
    def loop(self, *args):
        if self.parent.width < self.parent.height:
            self.width = self.parent.width
        else:
            self.width = self.parent.height
        self.height = self.width


class Logo(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_window_resize()
        Window.bind(on_resize=self.on_window_resize)
        
    def on_window_resize(self, *args):
        self.width = Window.width - dp(30)
        self.height = self.width / 1160 * 343
        while self.height > 0.3 * Window.height:
            self.height -= 1


class MenuBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_window_resize()
        Window.bind(on_resize=self.on_window_resize)
    
    def on_window_resize(self, *args):
        self.width = Window.width - dp(50)
        self.height = self.width / 1289 * 958
        while self.height > 0.6 * Window.height:
            self.height -= 1
        while self.width / 1289 * 958 > self.height:
            self.width -= 1


class CenterBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.orientation = "vertical"
        self.on_window_resize()
        Window.bind(on_resize=self.on_window_resize)
    
    def on_window_resize(self, *args):
        try:
            width = self.children[0].width
            self.width = width
            height = self.children[0].height + self.children[1].height
            self.height = height
        except:
            pass
        self.spacing = (Window.height - self.height) / 5
    
    def on_kv_post(self, base_widget):
        self.on_window_resize()


class CreditLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time = 0
        Clock.schedule_interval(self.loop, 1/5)
    
    def time_reset(self):
        self.time = 0
        self.color = (1, 1, 1)
    
    def loop(self, *args):
        self.time += 1
        if self.time == 50:
            self.color = (randint(0, 100)/100, randint(0, 100)/100, randint(0, 100)/100)
        elif self.time >= 56:
            self.time = 49