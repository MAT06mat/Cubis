import json
import os

from kivy.event import EventDispatcher


class Data(EventDispatcher):
    def __init__(self, file):
        self.path = os.path.join("assets", "data")
        self.file = file
    
    def get(self):
        with open(self.get_path(), encoding="UTF-8") as file:
            data = json.load(file)
        return data
    
    def get_path(self):
        # Obtenir le chemin absolu du répertoire "app/models"
        models_dir = os.path.dirname(os.path.abspath(__file__))
        # Obtenir le chemin absolu du répertoire "app"
        app_dir = os.path.dirname(models_dir)
        path = os.path.join(app_dir, self.path, self.file)
        return path