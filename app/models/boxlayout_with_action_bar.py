from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout

import os

current_directory = os.path.dirname(os.path.realpath(__file__))
kv_file_path = os.path.join(current_directory, "../views/boxlayout_with_action_bar.kv")
Builder.load_file(kv_file_path)

class BoxLayoutWithActionBar(BoxLayout):
    title = StringProperty()
