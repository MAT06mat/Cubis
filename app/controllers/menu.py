from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, RoundedRectangle, ContextInstruction
from kivy.metrics import dp
from kivy.properties import BooleanProperty
from random import randint
import webbrowser

from models.data import SETTINGS, TEXTS
from models.loop import Loop

# ============ SETTINGS ============

class CustomButton(Button):
    pass

class LButton(Button):
    current_lang = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        TEXTS.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.current_lang = TEXTS.uncomplete_lang(self.text) == TEXTS.current_lang
        with self.canvas.before:
            ContextInstruction()
            if self.current_lang:
                Color(0.72, 0.34, 0.05, 1)
                RoundedRectangle(pos=self.pos, size=self.size, radius=[5,])
                Color(0.82, 0.44, 0.15, 1)
                RoundedRectangle(pos=(self.x+2, self.y+2), size=(self.width-4, self.height-4),radius=[5,])
            else:
                Color(0.82, 0.44, 0.15, 1)
                RoundedRectangle(pos=self.pos, size=self.size, radius=[5,])
    
    def on_release(self):
        self.parent.parent.select(self.text)
        SETTINGS.modify(element=TEXTS.uncomplete_lang(self.text), key="lang")
        TEXTS.change_lang(TEXTS.uncomplete_lang(self.text))
        return super().on_release()


class LangButton(DropDown):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bnt_list = []
        for lang in TEXTS.langs():
            current_lang = TEXTS.uncomplete_lang(lang) == TEXTS.current_lang
            b = LButton(text=TEXTS.complete_lang(lang), size_hint_y=None, current_lang=current_lang)
            self.add_widget(b)
            self.bnt_list.append(b)
        self.select(SETTINGS.get()['lang'])


class DropButton(CustomButton, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        TEXTS.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.text = TEXTS.key(37)
        
    def loop(self, *args):
        credit_button = self.parent.ids.credit_button
        setting_image = self.parent.ids.setting_image
        musique_slider = self.parent.ids.musique_slider
        self.center_x = musique_slider.center_x
        self.y = setting_image.y + setting_image.width * 0.35
        self.width = credit_button.width * 3 / 2
        self.height = credit_button.height * 3 / 2
        for bnt in self.parent.dropdown.bnt_list:
            bnt.height = self.height / 2
            bnt.font_size = self.width / 10


class Setting(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.init, 0.1)
    
    def init(self, *args):
        #TEXTS.complete_lang(TEXTS.current_lang)
        self.mainbutton = DropButton(text=TEXTS.key(37), size_hint=(None, None))
        self.dropdown = LangButton()
        self.mainbutton.bind(on_release=self.dropdown.open)
        #self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        self.add_widget(self.mainbutton)
        self.add_widget(self.dropdown)


class CreditButton(CustomButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        TEXTS.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.text = TEXTS.key(30)


class PolicyButton(CustomButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        TEXTS.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.text = TEXTS.key(36)
    
    def on_press(self):
        webbrowser.open('https://mat06mat.github.io/matthieufelten/cubis-privacy-policy.html')
        return super().on_press()


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


class EffectsLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        TEXTS.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.text = TEXTS.key(29)
    
    
class MusicsLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        TEXTS.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.text = TEXTS.key(28)


class SettingImage(Image, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        TEXTS.bind(current_lang=self.lang_change)

    def lang_change(self, *args):
        self.source = TEXTS.image_path("assets/images/elements/setting.png")
        
    def loop(self, *args):
        if self.parent.width < self.parent.height:
            self.width = self.parent.width
        else:
            self.width = self.parent.height
        self.height = self.width

# ============ MAIN MENU ============

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


class SMButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        TEXTS.bind(current_lang=self.lang_change)

    def lang_change(self, *args):
        self.background_normal = TEXTS.image_path("assets/images/buttons/story_mode.png")
        self.background_down = TEXTS.image_path("assets/images/buttons/story_mode.png")


class IMButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        TEXTS.bind(current_lang=self.lang_change)

    def lang_change(self, *args):
        self.background_normal = TEXTS.image_path("assets/images/buttons/infinite_mode.png")
        self.background_down = TEXTS.image_path("assets/images/buttons/infinite_mode.png")

# ============ START ANIMATION ============

class StartImage(Image, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer = 0
        self.color = (1, 1, 1, 0)
    
    def loop(self, *args):
        self.timer += 1.5
        if self.timer > 100:
            self.timer = 100
        self.color = (1, 1, 1, self.timer/100)


class StartButton(Button, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wait = 120
    
    def loop(self, *args):
        self.wait -= 1
        if self.wait < 0:
            self.wait = 0
            self.disabled = False
    

class StartLabel(Label, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer = 100
        self.wait = 120
        self.lang_change()
        TEXTS.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.text = TEXTS.key(16)
    
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

# ============ CREDITS ============

class CreditLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.time = 0
        Clock.schedule_interval(self.loop, 1/5)
        self.lang_change()
        TEXTS.bind(current_lang=self.lang_change)
    
    def time_reset(self):
        self.time = 0
        self.color = (1, 1, 1)
    
    def lang_change(self, *args):
        self.text = TEXTS.key(31)
    
    def loop(self, *args):
        self.time += 1
        if self.time == 50:
            self.color = (randint(0, 100)/100, randint(0, 100)/100, randint(0, 100)/100)
        elif self.time >= 50:
            self.time = 49
    
    def on_ref_press(self, ref):
        webbrowser.open('https://https://mat06mat.github.io/matthieufelten/')
        return super().on_ref_press(ref)
