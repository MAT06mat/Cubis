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

from data.settings import Settings
from data.texts import Texts
from models.loop import Loop

# ============ SETTINGS ============

class CustomButton(Button):
    pass

class LButton(Button):
    current_lang = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Texts.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.current_lang = Texts.uncomplete_lang(self.text) == Texts.current_lang
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
        Texts.change_lang(Texts.uncomplete_lang(self.text))
        return super().on_release()


class LangButton(DropDown):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bnt_list = []
        for lang in Texts.lang_dict.keys():
            current_lang = lang == Texts.current_lang
            b = LButton(text=Texts.complete_lang(lang), size_hint_y=None, current_lang=current_lang)
            self.add_widget(b)
            self.bnt_list.append(b)
        self.select(Settings.lang)


class DropButton(CustomButton, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        Texts.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.text = Texts.key(37)
        
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


class FPSButton(CustomButton, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        Texts.bind(current_lang=self.lang_change)
        self.lang_change()
        Clock._max_fps = Settings.fps
    
    def lang_change(self, *args):
        if Settings.fps == 30:
            self.text = Texts.key(40)
        else:
            self.text = Texts.key(41)
    
    def on_press(self):
        if Settings.fps == 30:
            Settings.fps = 60
            Clock._max_fps = 60
        else:
            Settings.fps = 30
            Clock._max_fps = 30
        self.lang_change()
        return super().on_press()
        
    def loop(self, *args):
        self.center_x = self.parent.ids.effect_slider.center_x
        setting_image = self.parent.ids.setting_image
        self.y = setting_image.y + setting_image.width * 0.35
        self.size = self.parent.mainbutton.size


class Setting(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.init, -1)
    
    def init(self, *args):
        #TEXTS.complete_lang(TEXTS.current_lang)
        self.mainbutton = DropButton(text=Texts.key(37), size_hint=(None, None))
        self.dropdown = LangButton()
        self.mainbutton.bind(on_release=self.dropdown.open)
        self.fps_button = FPSButton()
        #self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))
        self.add_widget(self.mainbutton)
        self.add_widget(self.dropdown)
        self.add_widget(self.fps_button)


class CreditButton(CustomButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        Texts.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.text = Texts.key(30)


class PolicyButton(CustomButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        Texts.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.text = Texts.key(36)
    
    def on_press(self):
        webbrowser.open('https://mat06mat.github.io/matthieufelten/cubis-privacy-policy.html')
        return super().on_press()


class MusicSlider(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Settings.bind(is_init=self.init)
    
    def init(self, *args):
        self.value = Settings.music
    
    def on_value(self, *args):
        Settings.music = int(self.value)


class EffectSlider(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Settings.bind(is_init=self.init)
    
    def init(self, *args):
        self.value = Settings.effect
    
    def on_value(self, *args):
        Settings.effect = int(self.value)


class EffectsLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        Texts.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.text = Texts.key(29)
    
    
class MusicsLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        Texts.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.text = Texts.key(28)


class SettingImage(Image, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        Texts.bind(current_lang=self.lang_change)

    def lang_change(self, *args):
        self.source = Texts.image_path("assets/images/elements/setting.png")
        
    def loop(self, *args):
        if self.parent.width < self.parent.height:
            self.width = self.parent.width
        else:
            self.width = self.parent.height
        self.height = self.width

class BackMenuButton(Button, Loop):
    def loop(self, *args):
        if Window.width * 0.75 < Window.height:
            self.size_hint = (None, 0.07)
            self.width = self.height
        else:
            self.size_hint = (0.07, None)
            self.height = self.width
        return super().loop(*args)


class InfoLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Texts.bind(current_lang=self.lang_change)
        self.lang_change()
        Clock.schedule_interval(self.loop, 1)
        Clock._max_fps = 30
    
    def lang_change(self, *args):
        self.fps_name = Texts.key(42)
        self.version_name = Texts.key(43)

    def loop(self, *args):
        self.text = f"{self.fps_name}: {Clock.get_rfps()}    {self.version_name}: 1.5.2"

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
        Texts.bind(current_lang=self.lang_change)

    def lang_change(self, *args):
        self.background_normal = Texts.image_path("assets/images/buttons/story_mode.png")
        self.background_down = Texts.image_path("assets/images/buttons/story_mode.png")


class IMButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        Texts.bind(current_lang=self.lang_change)

    def lang_change(self, *args):
        self.background_normal = Texts.image_path("assets/images/buttons/infinite_mode.png")
        self.background_down = Texts.image_path("assets/images/buttons/infinite_mode.png")

# ============ START ANIMATION ============

class StartImage(Image):
    o = NumericProperty(-20)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Animation(duration=3, o=100).start(self)
        self.bind(o=self.opacity_update)
    
    def opacity_update(self, *args):
        self.color = (1, 1, 1, self.o/100)


class StartButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.undisabled, 4)
    
    def undisabled(self, *args):
        self.disabled = False
    

class StartLabel(Label, Loop):
    o = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        self.color = (1, 1, 1, 0)
        Texts.bind(current_lang=self.lang_change)
        self.anim = Animation(duration=1, o=80, t="in_out_sine") + Animation(duration=1, o=40, t="in_out_sine")
        self.anim.repeat = True
        Clock.schedule_once(self.start_anim, 3.5)
    
    def lang_change(self, *args):
        self.text = Texts.key(16)
    
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
        Texts.bind(current_lang=self.lang_change)
        self.last_event = Clock.schedule_once(self.wait_time, 10.0)
        self.last_event.cancel()
    
    def lang_change(self, *args):
        self.text = Texts.key(31)
    
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
