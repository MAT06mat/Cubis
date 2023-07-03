import json
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty

from infinite_mode import Cadre

Builder.load_file("message.kv")


class PlayButtonStory(Button):
    def __init__(self, id_level, **kwargs):
        super().__init__(**kwargs)
        self.id_level = id_level


class ModeLabel(Label):
    def __init__(self, mode, m=True, coeff_s=1/15, **kwargs):
        super().__init__(**kwargs)
        self.halign = "center"
        self.valign = "middle"
        self.coeff_s = coeff_s
        if m:
            self.pos_hint = {"center_x": 0.5, "center_y": 0.6}
            self.text = "Mode : " + mode[0]
            if len(mode) == 2:
                self.text += ", " + mode[1]
        else:
            self.pos_hint = {"center_x": 0.5, "center_y": 0.5}
            self.text = mode
        Clock.schedule_interval(self.loop, 1/60)
        
    def loop(self, *args):
        try:
            self.font_size = self.parent.width * self.coeff_s
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
        
        with open("data.json", "r") as data:
            self.data = json.load(data)
            areas = self.data["Areas"]
        for area in areas:
            for level in area["Levels"]:
                if level["Id"] == self.id_level:
                    mode = level["Mode"]
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
            with open("data.json", "r") as data:
                self.data = json.load(data)
                self.new_level = self.victoire == self.data["Current_level"]
            if self.new_level:
                self.data["Current_level"] += 1
                with open("data.json", "w") as data:
                    data.write(json.dumps(self.data))
            app = App.get_running_app()
            for screen in app.manager.screens:
                if screen.name == "StoryMode":
                    screen.children[0].children[0].reset()
        return super().on_press()


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
        with open("data.json") as data:
                self.data = json.load(data)
        current_level = self.data["Current_level"]
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
        self.label = ModeLabel(mode=self.message[0], m=False, coeff_s=1/15)
        self.add_widget(self.label)
    
    def on_window_resize(self, *args):
        self.width = Window.width
        self.height = self.width / 1894 * 1400
        while self.height > 0.5 * Window.height:
            self.height -= 1
        while self.width / 1894 * 1400 > self.height:
            self.width -= 1