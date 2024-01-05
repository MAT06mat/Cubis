from typing import Any
from kivy.core.audio import SoundLoader

from data.settings import Settings

import os


class Sound:
    def __init__(self, path, file) -> None:
        self.sound = SoundLoader.load(os.path.join(path, file))

    def play(self):
        self.sound.volume = Settings.effect / 100
        self.sound.play()


class DataSounds:
    def __init__(self) -> None:
        relative_path = os.path.join("assets", "sounds")
        # Obtenir le chemin absolu du répertoire "app/models"
        models_dir = os.path.dirname(os.path.abspath(__file__))
        # Obtenir le chemin absolu du répertoire "app"
        app_dir = os.path.dirname(models_dir)
        path = os.path.join(app_dir, relative_path)
        
        self.button = Sound(path, "button.wav")
        self.piece = Sound(path, "piece.wav")

    def __getattribute__(self, __name: str) -> Any:
        object.__getattribute__(self, __name).play()


Sounds = DataSounds()