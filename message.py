from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.metrics import dp

from infinite_mode import Cadre
from data import AREAS, SETTINGS

Builder.load_file("message.kv")


class PlayButtonStory(Button):
    def __init__(self, id_level, **kwargs):
        super().__init__(**kwargs)
        self.id_level = id_level


class Texte(Label):
    def __init__(self, middle=False, mode=None, **kwargs):
        super().__init__(**kwargs)
        self.halign = "center"
        self.valign = "middle"
        self.pos_hint = {"center_x": 0.5, "center_y": 0.6}
        if mode:
            self.text = "Mode : "
            for m in mode:
                if mode.index(m) > 0:
                    self.text += ", "
                self.text += m
        if middle:
            self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
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
    def __init__(self, id_level, **kw):
        super().__init__(**kw)
        self.id_level = id_level
        for area in AREAS.get("all"):
            for level in area["Levels"]:
                if level["Id"] == self.id_level:
                    mode = level["Mode"]
        self.add_widget(Cadre())
        self.add_widget(Back())
        self.add_widget(Title(text="Niveau "+str(id_level)))
        self.add_widget(Texte(mode=mode))
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
    def __init__(self, id_level, coeff_x=-0.7,**kwargs):
        super().__init__(**kwargs)
        self.id_level = id_level
        self.coeff_x = coeff_x
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        self.width = self.parent.height/3
        self.height = self.width
        self.y = self.parent.height/6
        self.x = Window.width/2 - self.width/2 + self.width*self.coeff_x


class QuitButton(Button):
    def __init__(self, coeff_x=0.7, coeff_h=1, new_image=None, victoire=False, **kwargs):
        super().__init__(**kwargs)
        self.coeff_x = coeff_x
        self.coeff_h = coeff_h
        self.new_image = new_image
        self.victoire = victoire
        if self.new_image:
            self.background_normal = self.new_image
            self.background_down = self.new_image
        else:
            self.background_normal = "images/buttons/quit.png"
            self.background_down = "images/buttons/quit.png"
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        if not self.new_image:
            self.height = self.parent.height/3*self.coeff_h
            self.width = self.height
        else:
            self.height = self.parent.height/3*self.coeff_h
            self.width = self.height/823*1886
        self.y = self.parent.height/6
        self.x = Window.width/2 - self.width/2 + self.width*self.coeff_x
    
    def on_press(self):
        if self.victoire != False:
            current_level = SETTINGS.get("Current_level")
            if self.victoire == current_level:
                SETTINGS.modify("Current_level", current_level+1)
            app = App.get_running_app()
            for screen in app.manager.screens:
                if screen.name == "StoryMode":
                    screen.children[0].children[0].reset()
        return super().on_press()


class MenuMessage(RelativeLayout):
    def __init__(self, id_level=0, mode=0, score=0, **kw):
        super().__init__(**kw)
        self.id_level = id_level
        self.mode = mode
        self.back = Back()
        self.cadre = Cadre()
        if self.id_level == 0:
            self.mode_label = Texte(text="Votre score : "+str(score))
            self.level_name = Title(text="Mode Infini")
        else:
            self.mode_label = Texte(mode=mode)
            self.level_name = Title(text="Niveau "+str(self.id_level))
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
    def __init__(self, id_level,**kw):
        super().__init__(**kw)
        self.id_level = id_level
        current_level = SETTINGS.get("Current_level")
        if id_level == current_level:
            self.victoire = (0.2, 0.95, "images/buttons/next.png", self.id_level)
            self.coeff_x = -0.9
            self.setting = False
        else:
            self.coeff_x = -0.7
            self.victoire = ()
            self.setting = True
        self.add_widget(Cadre())
        self.add_widget(Title(text="Victoire !"))
        self.quit_button = QuitButton(*self.victoire)
        self.add_widget(self.quit_button)
        self.reset_button = ResetButton(id_level=self.id_level, coeff_x=self.coeff_x)
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
    message = ("None")
    def __init__(self, message, title="Tutoriel",**kw):
        self.message = message
        self.title = title
        super().__init__(**kw)
        self.on_window_resize()
        Window.bind(on_resize=self.on_window_resize)
        Clock.schedule_once(self.add_label)

    def next(self):
        i = self.message.index(self.label.text)
        try:
            self.label.text = self.message[i+1]
        except:
            my = self.parent.message
            self.parent.message = None
            self.parent.remove_widget(my)
    
    def add_label(self, *args):
        self.label = Texte(text=self.message[0], middle=True)
        self.add_widget(self.label)
    
    def on_window_resize(self, *args):
        self.width = Window.width
        self.height = self.width / 1894 * 1400
        while self.height > 0.5 * Window.height:
            self.height -= 1
        while self.width / 1894 * 1400 > self.height:
            self.width -= 1