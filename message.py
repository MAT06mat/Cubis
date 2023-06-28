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


class Title(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
    def __init__(self, mode, id_level, **kw):
        super().__init__(**kw)
        self.add_widget(Cadre())
        self.add_widget(Back())
        self.add_widget(Title(text="Niveau "+str(id_level)))
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
    def __init__(self, id_level, mult_x=-0.7,**kwargs):
        super().__init__(**kwargs)
        self.id_level = id_level
        self.mult_x = mult_x
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        self.width = self.parent.height/3
        self.height = self.width
        self.y = self.parent.height/6
        self.x = Window.width/2 - self.width/2 + self.width*self.mult_x


class QuitButton(Button):
    def __init__(self, mult_x=0.7, mult_height=1, new_image=None, **kwargs):
        super().__init__(**kwargs)
        self.mult_x = mult_x
        self.mult_height = mult_height
        self.new_image = new_image
        if self.new_image:
            self.background_normal = self.new_image
            self.background_down = self.new_image
        else:
            self.background_normal = "images/buttons/quit.png"
            self.background_down = "images/buttons/quit.png"
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        if not self.new_image:
            self.height = self.parent.height/3*self.mult_height
            self.width = self.height
        else:
            self.height = self.parent.height/3*self.mult_height
            self.width = self.height/823*1886
        self.y = self.parent.height/6
        self.x = Window.width/2 - self.width/2 + self.width*self.mult_x


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
        self.level_name = Title(text="Niveau "+str(self.id_level))
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


class VictoireMessage(RelativeLayout):
    def __init__(self, id_level,**kw):
        super().__init__(**kw)
        self.id_level = id_level
        self.add_widget(Cadre())
        self.add_widget(Title(text="Victoire !"))
        self.quit_button = QuitButton(mult_x=0.2, mult_height=0.95, new_image="images/buttons/next.png")
        self.add_widget(self.quit_button)
        self.reset_button = ResetButton(id_level=self.id_level, mult_x=-0.9)
        self.add_widget(self.reset_button)
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