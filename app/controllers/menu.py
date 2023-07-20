from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from random import randint

from models.data import SETTINGS
from models.loop import Loop


class MusicSlider(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        SETTINGS.bind(is_init=self.init)
    
    def init(self, *args):
        self.value = SETTINGS.get()["Music"]
    
    def on_value(self, *args):
        SETTINGS.modify(element=int(self.value), key="Music")


class EffectSlider(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        SETTINGS.bind(is_init=self.init)
    
    def init(self, *args):
        self.value = SETTINGS.get()["Effect"]
    
    def on_value(self, *args):
        SETTINGS.modify(element=int(self.value), key="Effect")


class SettingImage(Image, Loop):
    def loop(self, *args):
        if self.parent.width < self.parent.height:
            self.width = self.parent.width
        else:
            self.width = self.parent.height
        self.height = self.width


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


class Presplash(Image, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer = 102
    
    def loop(self, *args):
        self.timer -= 3
        if self.timer < 0:
            self.timer = 0
        self.color = (1, 1, 1, self.timer/100)


class StartButton(Button, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer = 200
        self.o = 100
        self.wait = 220
        with self.canvas:
            Color(1, 1, 1, self.o/100)
            Rectangle(pos=self.pos, size=self.size)
    
    def loop(self, *args):
        self.timer -= 1
        self.o = self.timer
        if self.o >= 100:
            self.o = 100
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, self.o/100)
            Rectangle(pos=self.pos, size=self.size)
        self.wait -= 1
        if self.wait < 0:
            self.timer = 0
            self.wait = 0
            self.disabled = False
    

class StartLabel(Label, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer = 100
        self.wait = 230
    
    def loop(self, *args):
        # wait a the first delay
        self.wait -= 1
        if self.wait < 0:
            self.wait = 0
            self.timer += 0.5
            if self.timer == 70:
                self.timer = 130
            if self.timer == 200:
                self.timer = 0
            self.color = (1, 1, 1, abs(self.timer-100)/100)
            self.font_size = Window.width / 10
            self.width = Window.width - dp(20)
            self.height = self.width / 1289 * 554
        while self.height > 0.6 * Window.height:
            self.height -= 1
        while self.width / 1289 * 554 > self.height:
            self.width -= 1


class CenterBoxLayout(BoxLayout, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.orientation = "vertical"
    
    def loop(self, *args):
        try:
            width = self.children[0].width
            self.width = width
            height = self.children[0].height + self.children[1].height
            self.height = height
        except:
            pass
        self.spacing = (Window.height - self.height) / 5


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