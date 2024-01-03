from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.metrics import dp

from data import *
from models import *
from uix import *


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
        if self.height > 0.5 * Window.height:
            self.height = 0.5 * Window.height
        if self.width > self.height * 1894 / 1400:
            self.width = self.height * 1894 / 1400


class PlayInfiniteModeButton(CustomResizeButton, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.wait_end = True
        self.lang_change()
        Texts.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.source = Texts.image_path("atlas://assets/images/buttons/play")
    
    def loop(self, *args):
        self.width = Window.width - dp(50)
        self.height = self.width / 1192 * 501
        if self.height > 0.25 * Window.height:
            self.height =  0.25 * Window.height
        if self.width > self.height * 1192 / 501:
            self.width = self.height * 1192 / 501


class InfiniteMode(FloatLayout):
    message = None
    
    def message_push(self):
        if not self.message:
            self.message = InfoMessage(title=Texts.key(18), message=[Texts.key(44) + "\n\n[b]----- " + str(Settings.last_score) + " -----[/b]"], back=True, temp_parent=self)
            self.add_widget(self.message)
        else:
            self.message_pop()
            self.message_push()
    
    def message_pop(self):
        if self.message:
            self.remove_widget(self.message)
            self.message = None