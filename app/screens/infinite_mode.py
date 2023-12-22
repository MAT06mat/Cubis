from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.metrics import dp

from data import *
from models.loop import Loop


Builder.load_file("screens/infinite_mode.kv")


class ScoreListLabel(Label, Loop):
    def loop(self, *args):
        # add 0 before the score to have a 4-digit number
        text = Texts.key(8) + self.format_score(Settings.last_score) + Texts.key(9)
        for score in Settings.best_score:
            text = text + "\n - " + self.format_score(score)
        self.text = text

    def format_score(self, score):
        text = str(score)
        while len(text) < 4:
            text = "0" + text
        return text


class ScoreLayout(RelativeLayout, Loop):
    def loop(self, *args):
        self.width = Window.width - dp(30)
        self.height = self.width / 1894 * 1400
        while self.height > 0.5 * Window.height:
            self.height -= 1
        while self.width / 1894 * 1400 > self.height:
            self.width -= 1


class PlayInfiniteModeButton(Button, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang_change()
        Texts.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.background_normal = Texts.image_path("assets/images/buttons/play.png")
        self.background_down = Texts.image_path("assets/images/buttons/play.png")
    
    def loop(self, *args):
        self.width = Window.width - dp(30)
        self.height = self.width / 1192 * 501
        while self.height > 0.3 * Window.height:
            self.height -= 1
        while self.width / 1192 * 501 > self.height:
            self.width -= 1


class InfiniteMode(FloatLayout):
    def reload_image(self):
        image = self.ids.get("background_image")
        if image: image.reload()
