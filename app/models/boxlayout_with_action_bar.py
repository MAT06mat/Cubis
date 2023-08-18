from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

from models.data import TEXTS

import os

current_directory = os.path.dirname(os.path.realpath(__file__))
kv_file_path = os.path.join(current_directory, "../views/boxlayout_with_action_bar.kv")
Builder.load_file(kv_file_path)

class BoxLayoutWithActionBar(BoxLayout):
    title = StringProperty()
    title_key = StringProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        TEXTS.bind(current_lang=self.lang_change)
    
    def lang_change(self, *args):
        self.title = TEXTS.key(self.title_key)
        
