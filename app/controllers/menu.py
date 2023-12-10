from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, ContextInstruction
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.properties import BooleanProperty, NumericProperty
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
        Clock.schedule_once(self.init, -1)
    
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

class StartImage(Image):
    o = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Animation(duration=1.5, o=100).start(self)
        self.bind(o=self.opacity_update)
    
    def opacity_update(self, *args):
        self.color = (1, 1, 1, self.o/100)


class StartButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.undisabled, 2.5)
    
    def undisabled(self, *args):
        self.disabled = False
    

class StartLabel(Label, Loop):
    o = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        self.color = (1, 1, 1, 0)
        TEXTS.bind(current_lang=self.lang_change)
        self.anim = Animation(duration=1.5, o=80) + Animation(duration=1.5, o=40)
        self.anim.repeat = True
        Clock.schedule_once(self.start_anim, 2.5)
    
    def lang_change(self, *args):
        self.text = TEXTS.key(16)
    
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

# ============ CREDITS ============

class CreditLabel(Label, Loop):
    r = 255
    g = 255
    b = 255
    reload = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        TEXTS.bind(current_lang=self.lang_change)
        self.last_event = Clock.schedule_once(self.wait_time, 10.0)
        self.last_event.cancel()
    
    def lang_change(self, *args):
        self.text = TEXTS.key(31)
    
    def pre_enter(self):
        self.reload = False
        self.last_event.cancel()
        self.last_event = Clock.schedule_once(self.wait_time, 10.0)
    
    def wait_time(self, *args):
        self.reload = True
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        self.r += randint(-10, 10)
        self.g += randint(-10, 10)
        self.b += randint(-10, 10)
        if self.r > 200:
            self.r = 200
        if self.g > 200:
            self.g = 200
        if self.b > 200:
            self.b = 200
        if self.r < 50:
            self.r = 50
        if self.g < 50:
            self.g = 50
        if self.b < 50:
            self.b = 50
        self.color = (self.r/255, self.g/255, self.b/255, 1)
        if not self.reload:
            self.color = (1, 1, 1, 1)
        return super().loop(*args)
    
    def on_ref_press(self, ref):
        webbrowser.open('https://mat06mat.github.io/matthieufelten/')
        return super().on_ref_press(ref)
