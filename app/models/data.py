from kivy.app import App

import json
import os


class Data:
    path = os.path.join("assets", "data")
    path_rel = None
    
    def get(self, key: str):
        key = str(key)
        with open(self.get_path()) as file:
            data = json.load(file)
        if key == 'all':
            return data
        else:
            try:
                return data[key]
            except KeyError:
                return KeyError

    def modify(self, key: str, element):
        key = str(key)
        if key == 'all':
            data = element
        else:
            try:
                with open(self.get_path()) as file:
                    data = json.load(file)
                data[key] = element
            except KeyError:
                return KeyError
        with open(self.get_path(), "w") as file:
            file.write(json.dumps(data))
    
    def get_path(self):
        # Obtenez le chemin absolu du répertoire "app/models"
        models_dir = os.path.dirname(os.path.abspath(__file__))
        # Obtenez le chemin absolu du répertoire "app"
        app_dir = os.path.dirname(models_dir)
        path = os.path.join(app_dir, self.path, self.path_rel)
        return path


class SettingsData(Data):
    path_rel = "settings.json"

    def __init__(self):
        if 'ANDROID_ARGUMENT' in os.environ:
            app = App.get_running_app()
            app_private_dir = app.user_data_dir
        else:
            app_private_dir = os.path.join(os.path.expanduser('~'), '.cubis')
        data_folder_name = 'data_folder'
        self.path = os.path.join(app_private_dir, data_folder_name)
        
        # Si le dossier n'exite pas, on le créé
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        # Si le fichier n'exite pas, on le créé et on copy les data de base
        if not os.path.exists(self.get_path()):
            data = json.loads('{"Best_score": [0, 0, 0, 0, 0], "Last_score": 0, "Current_level": 1, "Music": 50, "Effect": 50}')
            with open(self.get_path(), 'w') as file:
                json.dump(data, file)
    
    def get_path(self):
        path = os.path.join(self.path, self.path_rel)
        return path


class AreasData(Data):
    path_rel = "areas.json"


class PiecesData(Data):
    path_rel = "pieces.json"


class LevelsData(Data):
    path_rel = "levels.json"


SETTINGS = SettingsData()
AREAS = AreasData()
PIECES = PiecesData()
LEVELS = LevelsData()