from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty, ListProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.app import App

from data.texts import Texts
from data.levels import Levels
from data.areas import Areas
from data.settings import Settings
from models.loop import Loop
from uix import *

import time


Builder.load_file("models/message.kv")


class Message(RelativeLayout):
    def __init__(self, temp_parent, **kw):
        super().__init__(**kw)
        self.on_window_resize()
        Window.bind(on_resize=self.on_window_resize)
        self.background_button = BackgroundButton(message=self)
        temp_parent.add_widget(self.background_button)
        self.temp_parent = temp_parent
        self.add_widget(Cadre())
    
    def on_parent(self, *args):
        if self.parent == None:
            self.temp_parent.remove_widget(self.background_button)
    
    def on_window_resize(self, *args):
        self.width = Window.width - dp(30)
        self.height = self.width / 1894 * 1400
        if self.height > 0.5 * Window.height:
            self.height = 0.5 * Window.height
        if self.width > self.height * 1894 / 1400:
            self.width = self.height * 1894 / 1400
    
    def message_pop(self):
        self.parent.message_pop()


class BackgroundButton(CustomPressButton):
    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.message = message
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 1)
        self.opacity = 0
        self.anim = Animation(d=0.2, opacity=0.3)
        self.anim.start(self)
        self.on_window_resize()
        Window.bind(on_resize=self.on_window_resize)
    
    def condition(self):
        for obj in self.message.children:
            if isinstance(obj, Back) and not self.message.collide_point(Window.mouse_pos[0]*dp(1), Window.mouse_pos[1]*dp(1)):
                return True
        if isinstance(self.message, InfoMessage) and not self.message.collide_point(Window.mouse_pos[0]*dp(1), Window.mouse_pos[1]*dp(1)):
            return True
        return False
    
    def on_custom_press(self, *args):
        for obj in self.message.children:
            if isinstance(obj, Back):
                self.message.temp_parent.message_pop()
                return super().on_custom_press(*args)
        if isinstance(self.message, InfoMessage):
            self.message.next()
        return super().on_custom_press(*args)
    
    def on_window_resize(self, *args):
        self.size = Window.size
        self.pos = (0, 0)


class PlayButtonStory(CustomResizeButton):
    id_level = NumericProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wait_end = True
        self.lang_change()
        try:
            Levels[str(self.id_level)]
        except KeyError:
            self.disabled = True
        Texts.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.source = Texts.image_path("atlas://assets/images/buttons/play")


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


class Back(CustomResizeButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = "atlas://assets/images/buttons/croix"
        self.size_hint = (None, None)
        self.pos_hint = {"right": 0.93, "top": 0.91}
        self.width = dp(35)
        self.height = self.width
    
    def loop(self, *args):
        self.width = self.parent.width/10
        self.height = self.width
        return super().loop(*args)
    
    def on_custom_press(self, *args):
        self.parent.message_pop()
        return super().on_custom_press(*args)


class PlayMessage(Message):
    id_level = NumericProperty(None)
    
    def __init__(self, **kw):
        super().__init__(**kw)
        for area in Areas:
            for level in area["Levels"]:
                if level["Id"] == self.id_level:
                    mode = level["Mode"]
        self.add_widget(Back())
        self.add_widget(Title(text_key=11, id_level=self.id_level))
        self.add_widget(Texte(mode=mode, font_size=self.width/15))
        self.add_widget(PlayButtonStory(id_level=self.id_level))


class SettingButton(CustomResizeButton):
    def loop(self, *args):
        self.width = self.parent.height/3.5
        self.height = self.width
        self.y = self.parent.height/6
        return super().loop(*args)


class ResetButton(CustomResizeButton):
    id_level = NumericProperty(None)
    
    def loop(self, *args):
        self.width = self.parent.height/3.5
        self.height = self.width
        self.y = self.parent.height/6
        return super().loop(*args)
    
    def on_custom_press(self, *args):
        if self.id_level == 0:
            Settings.last_score = self.parent.parent.score
            b = False
            for s in Settings.best_score:
                if Settings.last_score > s:
                    b = True
            app = App.get_running_app()
            if Settings.best_score[0] < Settings.last_score:
                    for screen in app.manager.screens:
                        if screen.name == "InfiniteMode":
                            screen.children[0].children[0].message_push()
            if b:
                best_score = list(Settings.best_score)
                best_score.append(Settings.last_score)
                sorted_list = list(sorted(best_score, reverse=True))
                sorted_list.pop(-1)
                Settings.best_score = sorted_list
        return super().on_custom_press(*args)


class QuitButton(CustomResizeButton):
    id_level = NumericProperty(0)
    victoire = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wait_end = True
        self.pos_hint = {"center_x": 0.75}
        if self.id_level != 0:
            self.coeff_h = 0.95
            self.pos_hint = {"center_x": 0.6}
            self.lang_change()
            Texts.bind(current_lang=self.lang_change)
        else:
            self.coeff_h = 1
            self.source = "atlas://assets/images/buttons/quit"

    def lang_change(self, *args):
        self.source = Texts.image_path("atlas://assets/images/buttons/next")
    
    def loop(self, *args):
        if self.id_level == 0:
            self.height = self.parent.height/3.5*self.coeff_h
            self.width = self.height
        else:
            self.height = self.parent.height/3.5*self.coeff_h
            self.width = self.height/823*1886
        self.y = self.parent.height/6
        return super().loop(*args)


class MenuMessage(Message):
    id_level = NumericProperty(0)
    score = NumericProperty(0)
    mode = ListProperty(None)
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.back = Back()
        if self.id_level != 0:
            self.level_name = Title(text_key=11, id_level=self.id_level)
            self.mode_label = Texte(mode=self.mode, font_size=self.width/15)
        else:
            self.level_name = Title(text_key=12)
            self.mode_label = Texte(text_key=13, score=self.score, font_size=self.width/15)
        self.quit_button = QuitButton()
        self.setting_button = SettingButton()
        self.reset_button = ResetButton(id_level=self.id_level)
        self.add_widget(self.back)
        self.add_widget(self.mode_label)
        self.add_widget(self.level_name)
        self.add_widget(self.quit_button)
        self.add_widget(self.setting_button)
        self.add_widget(self.reset_button)


class VictoireMessage(Message):
    id_level = NumericProperty(None)
    
    def __init__(self,**kw):
        super().__init__(**kw)
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


class NextButton(CustomResizeButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wait_end = True
        self.text = Texts.key(35)
    
    def on_custom_press(self, *args):
        self.parent.next()
        return super().on_custom_press(*args)


class InfoMessage(Message):
    message = ListProperty(None)
    
    def __init__(self, title=None, back=False, **kw):
        super().__init__(**kw)
        if not title:
            # Texts.key(15) -> "Tutoriel"
            title = Texts.key(15)
        self.title = Title(text=title)
        self.label = Texte(text=self.message[0], pos_hint={"center_x": 0.5, "center_y": 0.5}, font_size=self.width/15, markup=True)
        self.next_button = NextButton()
        self.add_widget(self.title)
        self.add_widget(self.label)
        self.add_widget(self.next_button)
        if back:
            self.back = Back()
            self.add_widget(self.back)

    def next(self):
        i = self.message.index(self.label.text)
        try:
            self.label.text = self.message[i+1]
        except:
            my = self.parent.message
            self.parent.message = None
            self.parent.remove_widget(my)


class ChoiceButton(CustomResizeButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wait_end = True


class YesButton(ChoiceButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = Texts.key(48)
        self.pos_hint = {"center_x": 0.35, "center_y": 0.2}
    
    def on_custom_press(self, *args):
        self.parent.on_yes_press()
        return super().on_custom_press(*args)


class NoButton(ChoiceButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = Texts.key(49)
        self.pos_hint = {"center_x": 0.65, "center_y": 0.2}
    
    def on_custom_press(self, *args):
        self.parent.on_no_press()
        return super().on_custom_press(*args)


class HelpMessage(Message, Loop):
    def __init__(self, temp_parent, **kw):
        super().__init__(temp_parent, **kw)
        self.back = Back()
        self.title = Title(text_key=45)
        self.yes_button = None
        self.no_button = None
        if Settings.nb_hint > 0:
            text = Texts.key(46) + str(Settings.nb_hint) + Texts.key(47)
            self.yes_button = YesButton()
            self.no_button = NoButton()
            self.add_widget(self.yes_button)
            self.add_widget(self.no_button)
        else:
            text = self.get_text_next_hint_time()
        self.label = Texte(text=text, pos_hint={"center_x": 0.5, "center_y": 0.5}, font_size=self.width/15)
        self.add_widget(self.back)
        self.add_widget(self.title)
        self.add_widget(self.label)
    
    def get_text_next_hint_time(self):
        next_time = int(Settings.next_hint_time - time.time())
        m = str(next_time//60)
        if len(m) == 1:
            m = "0" + m
        s = str(next_time%60)
        if len(s) == 1:
            s = "0" + s
        return f'{Texts.key(50)}\n{Texts.key(51)} {m}:{s}'
    
    def loop(self, *args) -> bool:
        if Settings.nb_hint == 0:
            self.label.text = self.get_text_next_hint_time()
        else:
            if not self.yes_button:
                self.label.text = Texts.key(46) + str(Settings.nb_hint) + Texts.key(47)
                self.yes_button = YesButton()
                self.no_button = NoButton()
                self.add_widget(self.yes_button)
                self.add_widget(self.no_button)
        return super().loop(*args)
    
    def on_yes_press(self):
        try:
            used = self.parent.use_hint()
        except:
            used = "error"
        
        self.parent.message_pop()
        
        if used != True:
            self.temp_parent.message_push(used)
    
    def on_no_press(self):
        self.parent.message_pop()