from kivy.uix.image import Image
from kivy.lang import Builder

import os

current_directory = os.path.dirname(os.path.realpath(__file__))
kv_file_path = os.path.join(current_directory, "../views/cadre.kv")
Builder.load_file(kv_file_path)


class Cadre(Image):
    pass