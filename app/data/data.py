import json
import os

from kivy.event import EventDispatcher


class Data(EventDispatcher):
    def __init__(self, file):
        self.relative_path = os.path.join("assets", "json")
        self.file = file
    
    def get(self, value=None):
        with open(self.path, encoding="UTF-8") as file:
            data = json.load(file)
        if value:
            return data[value]
        return data
    
    @property
    def path(self) -> str:
        # Obtenir le chemin absolu du répertoire "app/models"
        models_dir = os.path.dirname(os.path.abspath(__file__))
        # Obtenir le chemin absolu du répertoire "app"
        app_dir = os.path.dirname(models_dir)
        path = os.path.join(app_dir, self.relative_path, self.file)
        return path