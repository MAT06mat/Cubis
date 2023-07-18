from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty, ListProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.metrics import dp

from app.models.cadre import Cadre
from app.models.data import AREAS, SETTINGS

import os

current_directory = os.path.dirname(os.path.realpath(__file__))
kv_file_path = os.path.join(current_directory, "../views/message.kv")
Builder.load_file(kv_file_path)


class PlayButtonStory(Button):
    id_level = NumericProperty(None)


class Texte(Label):
    halign = "center"
    valign = "middle"
    pos_hint = {"center_x": 0.5, "center_y": 0.6}
    mode = ListProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.mode:
            self.text = "Mode : "
            for m in self.mode:
                if self.mode.index(m) > 0:
                    self.text += ", "
                self.text += m
        Clock.schedule_interval(self.loop, 1/60)
        
    def loop(self, *args):
        try:
            self.font_size = self.parent.width/15
        except:
            pass


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
    id_level = NumericProperty(None)
    
    def __init__(self, **kw):
        super().__init__(**kw)
        for area in AREAS.get("all"):
            for level in area["Levels"]:
                if level["Id"] == self.id_level:
                    mode = level["Mode"]
        self.add_widget(Cadre())
        self.add_widget(Back())
        self.add_widget(Title(text="Niveau "+str(self.id_level)))
        self.add_widget(Texte(mode=mode))
        self.add_widget(PlayButtonStory(id_level=self.id_level))
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
    id_level = NumericProperty(None)
    coeff_x = NumericProperty(-0.7)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        self.width = self.parent.height/3
        self.height = self.width
        self.y = self.parent.height/6
        self.x = Window.width/2 - self.width/2 + self.width*self.coeff_x


class QuitButton(Button):
    id_level = NumericProperty(0)
    victoire = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.id_level != 0:
            self.coeff_x = 0.2
            self.coeff_h = 0.95
            self.background_normal = "images/buttons/next.png"
            self.background_down = "images/buttons/next.png"
        else:
            self.coeff_x = 0.7
            self.coeff_h = 1
            self.background_normal = "images/buttons/quit.png"
            self.background_down = "images/buttons/quit.png"
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        if self.id_level == 0:
            self.height = self.parent.height/3*self.coeff_h
            self.width = self.height
        else:
            self.height = self.parent.height/3*self.coeff_h
            self.width = self.height/823*1886
        self.y = self.parent.height/6
        self.x = Window.width/2 - self.width/2 + self.width*self.coeff_x


class MenuMessage(RelativeLayout):
    id_level = NumericProperty(0)
    score = NumericProperty(0)
    mode = ListProperty(None)
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.back = Back()
        self.cadre = Cadre()
        if self.id_level != 0:
            self.level_name = Title(text="Niveau "+str(self.id_level))
            self.mode_label = Texte(mode=self.mode)
        else:
            self.level_name = Title(text="Mode Infini")
            self.mode_label = Texte(text="Votre score : "+str(self.score))
        self.quit_button = QuitButton()
        self.setting_button = SettingButton()
        self.reset_button = ResetButton(id_level=self.id_level)
        self.add_widget(self.cadre)
        self.add_widget(self.back)
        self.add_widget(self.mode_label)
        self.add_widget(self.level_name)
        self.add_widget(self.quit_button)
        self.add_widget(self.setting_button)
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
    id_level = NumericProperty(None)
    
    def __init__(self,**kw):
        super().__init__(**kw)
        if self.id_level == SETTINGS.get("Current_level"):
            self.quit_button = QuitButton(id_level=self.id_level, victoire=True)
            self.coeff_x = -0.9
            self.setting = False
        else:
            self.coeff_x = -0.7
            self.quit_button = QuitButton()
            self.setting = True
        self.reset_button = ResetButton(id_level=self.id_level, coeff_x=self.coeff_x)
        self.add_widget(Cadre())
        self.add_widget(Title(text="Victoire !"))
        self.add_widget(Texte(text="Niveau " + str(self.id_level)))
        self.add_widget(self.quit_button)
        self.add_widget(self.reset_button)
        if self.setting:
            self.add_widget(SettingButton())
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


class InfoMessage(RelativeLayout):
    message = ListProperty(None)
    title = StringProperty("Tutoriel")
    
    def __init__(self,**kw):
        super().__init__(**kw)
        self.label = Texte(text=self.message[0], pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.add_widget(self.label)
        self.on_window_resize()
        Window.bind(on_resize=self.on_window_resize)

    def next(self):
        i = self.message.index(self.label.text)
        try:
            self.label.text = self.message[i+1]
        except:
            my = self.parent.message
            self.parent.message = None
            self.parent.remove_widget(my)
    
    def on_window_resize(self, *args):
        self.width = Window.width
        self.height = self.width / 1894 * 1400
        while self.height > 0.5 * Window.height:
            self.height -= 1
        while self.width / 1894 * 1400 > self.height:
            self.width -= 1