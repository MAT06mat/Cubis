import json
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.metrics import dp
from infinite_mode import Cadre

Builder.load_file("message.kv")


class PlayButtonStory(Button):
    pass


class ModeLabel(Label):
    def __init__(self, mode, **kwargs):
        super().__init__(**kwargs)
        self.text = "Mode : " + mode[0]
        if len(mode) == 2:
            self.text += ", " + mode[1]
        Window.bind(on_resize=self.on_window_resize)
        Clock.schedule_once(lambda dt: self.on_window_resize())
        
    def on_window_resize(self, *args):
        self.font_size = self.parent.width / 15


class LevelName(Label):
    def __init__(self, text_var, **kwargs):
        super().__init__(**kwargs)
        self.text = "Niveau " + text_var
        Window.bind(on_resize=self.on_window_resize)
        Clock.schedule_once(lambda dt: self.on_window_resize())
        
    def on_window_resize(self, *args):
        self.font_size = self.parent.width / 8


class Back(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = "images/buttons/croix.png"
        self.background_down = "images/buttons/croix.png"
        self.size_hint = (None, None)
        Window.bind(on_resize=self.on_window_resize)
        Clock.schedule_once(lambda dt: self.on_window_resize())
        
    def on_window_resize(self, *args):
        w, h = self.parent.size
        self.width = w/1894*300
        self.height = self.width
        self.pos = (w-w/4.8, h-h/3.5)
    
    def on_press(self):
        self.parent.message_pop()
        return super().on_press()

class PlayMessage(RelativeLayout):
    def __init__(self, text_var, mode, **kw):
        super().__init__(**kw)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        self.size_hint = (None, None)
        self.add_widget(Cadre())
        self.add_widget(Back())
        self.add_widget(LevelName(text_var=text_var))
        self.add_widget(ModeLabel(mode=mode))
        self.add_widget(PlayButtonStory())
        self.on_window_resize()
        Window.bind(on_resize=self.on_window_resize)
    
    def on_window_resize(self, *args):
        self.width = Window.width - dp(30)
        self.height = self.width / 1894 * 1400
        while self.height > 0.5 * Window.height:
            self.height -= 1
        while self.width / 1894 * 1400 > self.height:
            self.width -= 1
    
    def message_pop(self):
        self.parent.message_pop()