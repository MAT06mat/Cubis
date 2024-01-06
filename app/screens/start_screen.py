from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.properties import NumericProperty
from kivy.lang import Builder
from kivy.app import App

from data import *
from models import *
from uix import *


Builder.load_file("screens/start_screen.kv")


# ============ START SCREEN ============


class StartImage(Image):
    o = NumericProperty(-20)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Animation(duration=3, o=100).start(self)
        self.bind(o=self.opacity_update)
    
    def opacity_update(self, *args):
        self.color = (1, 1, 1, self.o/100)


class StartButton(CustomPressButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.undisabled, 5.5)
    
    def undisabled(self, *args):
        self.disabled = False


class StartLabel(Label, Loop):
    o = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        self.color = (1, 1, 1, 0)
        Texts.bind(current_lang=self.lang_change)
        self.anim = Animation(duration=1, o=80, t="in_out_sine") + Animation(duration=1, o=40, t="in_out_sine")
        self.anim.repeat = True
        Clock.schedule_once(self.start_anim, 5)
    
    def lang_change(self, *args):
        self.text = Texts.key(16)
    
    def start_anim(self, *args):
        self.anim.start(self)
    
    def loop(self, *args):
        self.color = (1, 1, 1, self.o/100)
        if Window.width < dp(500):
            self.font_size = Window.width/10
        else:
            self.font_size = dp(50)


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