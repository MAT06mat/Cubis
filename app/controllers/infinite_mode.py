from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.metrics import dp

from models.data import SETTINGS
from models.loop import Loop

import os

current_directory = os.path.dirname(os.path.realpath(__file__))
kv_file_path = os.path.join(current_directory, "../views/infinite_mode.kv")
Builder.load_file(kv_file_path)


class ScoreListLabel(Label, Loop):
    def loop(self, *args):
        # add 0 before the score to have a 4-digit number
        self.best_score = SETTINGS.get()["Best_score"]
        self.last_score = SETTINGS.get()["Last_score"]
        text = "Votre dernier score : " + self.format_score(self.last_score) + "\nVos meilleurs scores : "
        for score in self.best_score:
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
    def loop(self, *args):
        self.width = Window.width - dp(30)
        self.height = self.width / 1192 * 501
        while self.height > 0.3 * Window.height:
            self.height -= 1
        while self.width / 1192 * 501 > self.height:
            self.width -= 1


class InfiniteMode(FloatLayout):
    pass
