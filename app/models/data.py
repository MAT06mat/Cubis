import json
import os

from kivy.properties import BooleanProperty
from kivy.event import EventDispatcher

class Data(EventDispatcher):
    is_init = BooleanProperty(False)
    
    def __init__(self, file):
        self.path = os.path.join("assets", "data")
        self.file = file

    def init_with_user_data_dir(self, user_data_dir):
        if 'ANDROID_ARGUMENT' in os.environ:
            app_private_dir = user_data_dir
            data_folder_name = '.cubis'
            path = os.path.join(app_private_dir, data_folder_name)
        else:
            path = os.path.join(os.path.expanduser('~'), '.cubis')
        # Si le dossier n'exite pas, on le créé
        if not os.path.exists(path):
            os.makedirs(path)
        # Si le fichier n'exite pas, on le créé et on copy les data de base
        if not os.path.exists(os.path.join(path, self.file)):
            with open(os.path.join(path, self.file), 'w') as file:
                file.write('{"Best_score": [0, 0, 0, 0, 0], "Last_score": 0, "Current_level": 1, "Music": 50, "Effect": 50}')
        self.path = path
        self.is_init = True
    
    def get(self):
        with open(self.get_path()) as file:
            data = json.load(file)
        return data

    def modify(self, element, key='all'):
        key = str(key)
        if key == 'all':
            data = element
        else:
            with open(self.get_path()) as file:
                data = json.load(file)
            if key in data:
                data[key] = element
            else:
                return KeyError
        with open(self.get_path(), "w") as file:
            file.write(json.dumps(data))
    
    def get_path(self):
        if self.file == 'settings.json':
            path = os.path.join(self.path, self.file)
        else:
            # Obtenez le chemin absolu du répertoire "app/models"
            models_dir = os.path.dirname(os.path.abspath(__file__))
            # Obtenez le chemin absolu du répertoire "app"
            app_dir = os.path.dirname(models_dir)
            path = os.path.join(app_dir, self.path, self.file)
        return path


SETTINGS = Data(file='settings.json')
AREAS = Data(file='areas.json')
PIECES = Data(file='pieces.json')
LEVELS = Data(file='levels.json')