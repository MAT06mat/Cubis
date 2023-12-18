from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty, ListProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.metrics import dp

from data.settings import Settings
from data.areas import Areas
from data.levels import Levels
from data.texts import Texts
from uix.cadre import Cadre
from models.loop import Loop


Builder.load_file("models/message.kv")


class Message(RelativeLayout):
    pass


class PlayButtonStory(Button):
    id_level = NumericProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        try:
            Levels.get(self.id_level)
        except KeyError:
            self.disabled = True
        Texts.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.background_normal = Texts.image_path("assets/images/buttons/play.png")
        self.background_down = Texts.image_path("assets/images/buttons/play.png")
        self.background_disabled_normal = Texts.image_path("assets/images/buttons/play-disabled.png")


class Texte(Label, Loop):
    halign = "center"
    valign = "middle"
    pos_hint = {"center_x": 0.5, "center_y": 0.6}
    mode = ListProperty(None)
    
    def __init__(self, text_key=None, score=None, **kwargs):
        super().__init__(**kwargs)
        self.text_key = text_key
        self.score = score
        self.lang_change()
        Texts.bind(current_lang=self.lang_change)
        Clock.schedule_once(self.init_font_size, -1)
    
    def lang_change(self, *args):
        if self.mode:
            self.text = Texts.key(10)
            for m in self.mode:
                if self.mode.index(m) > 0:
                    self.text += ", "
                if len(self.mode) > 2 and self.mode.index(m) == 1:
                    self.text += "\n"
                self.text += Texts.key(m)
        if self.text_key:
            self.text = Texts.key(self.text_key)
            if self.score != None:
                self.text += str(self.score)
    
    def init_font_size(self, *args):
        self.parent.bind(width=self.width_change)
    
    def width_change(self, *args):
        self.font_size = self.parent.width/15


class Title(Label, Loop):
    def __init__(self, text_key=None, id_level=None, **kwargs):
        super().__init__(**kwargs)
        self.text_key = text_key
        self.id_level = id_level
        self.lang_change()
        Texts.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        if self.text_key:
            if self.id_level:
                self.text = Texts.key(self.text_key) + str(self.id_level)
            else:
                self.text = Texts.key(self.text_key)
        
    def loop(self, *args):
        self.font_size = self.parent.width / 8


class Back(Button, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.width = dp(40)
        self.height = self.width
        
    def loop(self, *args):
        self.width = self.parent.width/8
        self.height = self.width
    
    def on_press(self):
        self.parent.message_pop()
        return super().on_press()

class PlayMessage(Message):
    id_level = NumericProperty(None)
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.on_window_resize()
        Window.bind(on_resize=self.on_window_resize)
        for area in Areas.get():
            for level in area["Levels"]:
                if level["Id"] == self.id_level:
                    mode = level["Mode"]
        self.add_widget(Cadre())
        self.add_widget(Back())
        self.add_widget(Title(text_key=11, id_level=self.id_level))
        self.add_widget(Texte(mode=mode, font_size=self.width/15))
        self.add_widget(PlayButtonStory(id_level=self.id_level))
    
    def on_window_resize(self, *args):
        self.width = Window.width - dp(30)
        self.height = self.width / 1894 * 1400
        while self.height > 0.5 * Window.height:
            self.height -= 1
        while self.width / 1894 * 1400 > self.height:
            self.width -= 1
    
    def message_pop(self):
        self.parent.message_pop()


class SettingButton(Button, Loop):
    def loop(self, *args):
        self.width = self.parent.height/3
        self.height = self.width
        self.y = self.parent.height/6


class ResetButton(Button, Loop):
    id_level = NumericProperty(None)
    
    def loop(self, *args):
        self.width = self.parent.height/3
        self.height = self.width
        self.y = self.parent.height/6
    
    def on_press(self):
        if self.id_level == 0:
            Settings.last_score = self.parent.parent.score
            b = False
            for s in Settings.best_score:
                if self.parent.parent.score > s:
                    b = True
            if b:
                best_score = list(Settings.best_score)
                best_score.append(self.parent.parent.score)
                sorted_list = list(sorted(best_score, reverse=True))
                sorted_list.pop(-1)
                Settings.best_score = sorted_list
        return super().on_press()


class QuitButton(Button, Loop):
    id_level = NumericProperty(0)
    victoire = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {"center_x": 0.75}
        if self.id_level != 0:
            self.coeff_h = 0.95
            self.pos_hint = {"center_x": 0.6}
            self.lang_change()
            Texts.bind(current_lang=self.lang_change)
        else:
            self.coeff_h = 1
            self.background_normal = "assets/images/buttons/quit.png"
            self.background_down = "assets/images/buttons/quit.png"

    def lang_change(self, *args):
        self.background_normal = Texts.image_path("assets/images/buttons/next.png")
        self.background_down = Texts.image_path("assets/images/buttons/next.png")
    
    def loop(self, *args):
        if self.id_level == 0:
            self.height = self.parent.height/3*self.coeff_h
            self.width = self.height
        else:
            self.height = self.parent.height/3*self.coeff_h
            self.width = self.height/823*1886
        self.y = self.parent.height/6


class MenuMessage(Message, Loop):
    id_level = NumericProperty(0)
    score = NumericProperty(0)
    mode = ListProperty(None)
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.back = Back()
        self.cadre = Cadre()
        if self.id_level != 0:
            self.level_name = Title(text_key=11, id_level=self.id_level)
            self.mode_label = Texte(mode=self.mode, font_size=self.width/15)
        else:
            self.level_name = Title(text_key=12)
            self.mode_label = Texte(text_key=13, score=self.score, font_size=self.width/15)
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
    
    def loop(self, *args):
        self.width = Window.width - dp(30)
        self.height = self.width / 1894 * 1400
        while self.height > 0.5 * Window.height:
            self.height -= 1
        while self.width / 1894 * 1400 > self.height:
            self.width -= 1
    
    def message_pop(self):
        self.parent.message_pop()


class VictoireMessage(Message):
    id_level = NumericProperty(None)
    
    def __init__(self,**kw):
        super().__init__(**kw)
        self.on_window_resize()
        Window.bind(on_resize=self.on_window_resize)
        self.add_widget(Cadre())
        self.add_widget(Title(text_key=14))
        self.add_widget(Texte(text_key=11, score=self.id_level, font_size=self.width/15))
        if self.id_level == Settings.current_level:
            Settings.current_level += 1
            self.quit_button = QuitButton(id_level=self.id_level, victoire=True)
        else:
            self.quit_button = QuitButton()
            self.add_widget(SettingButton())
        self.reset_button = ResetButton(id_level=self.id_level)
        self.add_widget(self.quit_button)
        self.add_widget(self.reset_button)
    
    def on_window_resize(self, *args):
        self.width = Window.width - dp(30)
        self.height = self.width / 1894 * 1400
        while self.height > 0.5 * Window.height:
            self.height -= 1
        while self.width / 1894 * 1400 > self.height:
            self.width -= 1
    
    def message_pop(self):
        self.parent.message_pop()


class NextButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = Texts.key(35)


class InfoMessage(Message):
    message = ListProperty(None)
    title = StringProperty(Texts.key(15))
    
    def __init__(self,**kw):
        super().__init__(**kw)
        self.on_window_resize()
        Window.bind(on_resize=self.on_window_resize)
        self.label = Texte(text=self.message[0], pos_hint={"center_x": 0.5, "center_y": 0.5}, font_size=self.width/15)
        self.add_widget(self.label)

    def next(self):
        i = self.message.index(self.label.text)
        try:
            self.label.text = self.message[i+1]
        except:
            my = self.parent.message
            self.parent.message = None
            self.parent.remove_widget(my)
    
    def on_window_resize(self, *args):
        self.width = Window.width - dp(30)
        self.height = self.width / 1894 * 1400
        while self.height > 0.5 * Window.height:
            self.height -= 1
        while self.width / 1894 * 1400 > self.height:
            self.width -= 1