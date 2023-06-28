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
    def __init__(self, id_level, **kwargs):
        super().__init__(**kwargs)
        self.id_level = id_level


class ModeLabel(Label):
    def __init__(self, mode, **kwargs):
        super().__init__(**kwargs)
        self.text = "Mode : " + mode[0]
        if len(mode) == 2:
            self.text += ", " + mode[1]
        Clock.schedule_interval(self.loop, 1/60)
        
    def loop(self, *args):
        self.font_size = self.parent.width / 15


class LevelName(Label):
    def __init__(self, text_var, **kwargs):
        super().__init__(**kwargs)
        self.text = "Niveau " + str(text_var)
        Clock.schedule_interval(self.loop, 1/60)
        
    def loop(self, *args):
        self.font_size = self.parent.width / 8


class Back(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.loop, 1/60)
        
    def loop(self, *args):
        self.width = self.parent.width/6
        self.height = self.width
    
    def on_press(self):
        self.parent.message_pop()
        return super().on_press()

class PlayMessage(RelativeLayout):
    def __init__(self, text_var, mode, id_level, **kw):
        super().__init__(**kw)
        self.add_widget(Cadre())
        self.add_widget(Back())
        self.add_widget(LevelName(text_var=text_var))
        self.add_widget(ModeLabel(mode=mode))
        self.add_widget(PlayButtonStory(id_level=id_level))
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


class SettingButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        self.width = self.parent.height/3
        self.height = self.width
        self.y = self.parent.height/6


class ResetButton(Button):
    def __init__(self, id_level, **kwargs):
        super().__init__(**kwargs)
        self.id_level = id_level
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        self.width = self.parent.height/3
        self.height = self.width
        self.y = self.parent.setting_button.y
        self.x = self.parent.setting_button.x - self.width*0.7


class QuitButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        self.width = self.parent.height/3
        self.height = self.width
        self.y = self.parent.setting_button.y
        self.x = self.parent.setting_button.x + self.width*0.7


class MenuMessage(RelativeLayout):
    def __init__(self, id_level, mode, **kw):
        super().__init__(**kw)
        self.id_level = id_level
        self.mode = mode
        self.cadre = Cadre()
        self.add_widget(self.cadre)
        self.back = Back()
        self.add_widget(self.back)
        self.mode_label = ModeLabel(mode=mode)
        self.add_widget(self.mode_label)
        self.level_name = LevelName(text_var=self.id_level)
        self.add_widget(self.level_name)
        self.quit_button = QuitButton()
        self.add_widget(self.quit_button)
        self.setting_button = SettingButton()
        self.add_widget(self.setting_button)
        self.reset_button = ResetButton(id_level=self.id_level)
        self.add_widget(self.reset_button)
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        self.height = self.width / 1894 * 1400
        while self.height > 0.5 * Window.height:
            self.height -= 1
        while self.width / 1894 * 1400 > self.height:
            self.width -= 1
    
    def message_pop(self):
        self.parent.message_pop()