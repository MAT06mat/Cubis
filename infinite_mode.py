from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.metrics import dp
import json

Builder.load_file("infinite_mode.kv")


class Cadre(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = "images/elements/frame.png"


class ScoreLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_score()
        Clock.schedule_interval(self.load_score, 1/60)
    
    def load_score(self, *args):
        # add 0 before the score to have a 4-digit number
        data = open("data.json")
        data_open = json.load(data)
        data.close()
        self.best_score = data_open["Best_score"]
        self.last_score = data_open["Last_score"]
        text = "Votre dérnier score : " + self.format_score(self.last_score) + "\nVos meilleurs scores : "
        for score in self.best_score:
            text = text + "\n - " + self.format_score(score)
        self.text = text

    def format_score(self, score):
        text = str(score)
        while len(text) < 4:
            text = "0" + text
        return text
        
        
class Score(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_window_resize()
        Window.bind(on_resize=self.on_window_resize)
    
    def on_window_resize(self, *args):
        self.width = Window.width - dp(30)
        self.height = self.width / 1894 * 1400
        while self.height > 0.5 * Window.height:
            self.height -= 1
        while self.width / 1894 * 1400 > self.height:
            self.width -= 1
    

class PlayButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_window_resize()
        Window.bind(on_resize=self.on_window_resize)
    
    def on_window_resize(self, *args):
        self.width = Window.width - dp(30)
        self.height = self.width / 1192 * 501
        while self.height > 0.3 * Window.height:
            self.height -= 1
        while self.width / 1192 * 501 > self.height:
            self.width -= 1
            


class InfiniteMode(FloatLayout):
    pass
