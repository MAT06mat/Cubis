import json
import os

from kivy.properties import BooleanProperty, StringProperty
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
            with open(os.path.join(path, self.file), 'w', encoding="UTF-8") as file:
                file.write('{"Best_score": [0, 0, 0, 0, 0], "Last_score": 0, "Current_level": 1, "Music": 50, "Effect": 50, "lang": "en"}')
        self.path = path
        self.is_init = True
    
    def get(self):
        with open(self.get_path(), encoding="UTF-8") as file:
            data = json.load(file)
        return data

    def modify(self, element, key='all'):
        key = str(key)
        if key == 'all':
            data = element
        else:
            with open(self.get_path(), encoding="UTF-8") as file:
                data = json.load(file)
            data[key] = element
        with open(self.get_path(), "w", encoding="UTF-8") as file:
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

class Texts(Data):
    current_lang = StringProperty("en")
    
    def __init__(self, file):
        super().__init__(file)
        SETTINGS.bind(is_init=self.setting_change)
    
    def setting_change(self, *args):
        if 'lang' in SETTINGS.get():
            self.current_lang = SETTINGS.get()['lang']
        else:
            SETTINGS.modify(element='en', key='lang')
            self.current_lang = "en"
        
    def key(self, key):
        key = str(key)
        for texts in self.get():
            if texts["lang"] == self.current_lang:
                if key in texts:
                    text = texts[key]
                    return text
                else:
                    return KeyError
    
    def change_lang(self, new_lang):
        if new_lang in self.langs():
            self.current_lang = new_lang
        else:
            return KeyError
    
    def langs(self):
        my_langs = list()
        for langs in self.get():
            my_langs.append(langs["lang"])
        return my_langs

    def image_path(self, path: str):
        path = path.split(".")
        if len(path) != 2:
            return ValueError
        path = f'{path[0]}-{self.current_lang}.{path[1]}'
        return path


TEXTS = Texts(file="texts.json")