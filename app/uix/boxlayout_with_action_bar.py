from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.metrics import dp

from data.texts import Texts


Builder.load_file("uix/boxlayout_with_action_bar.kv")


class BoxLayoutWithActionBar(BoxLayout):
    title = StringProperty()
    title_key = StringProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Texts.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.title = Texts.key(self.title_key)


class MyBar(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.height = dp(50)