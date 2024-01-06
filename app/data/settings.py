import shutil
import json
import os

from kivy.app import App
from kivy.properties import BooleanProperty

from data.data import Data


global Path
Path = None


class setting_propertie:
    value = None
    
    def __init__(self, name, default) -> None:
        self.name = name
        self.default = default
    
    def __get__(self, __instance, __owner=None):
        if not Path:
            print("[WARNING]: class", str(self) + ", get None because Path = None")
            return None
        if not self.value:
            with open(Path, encoding="UTF-8") as file:
                data = json.load(file)
            if self.name in data:
                self.value = data[self.name]
                return self.value
            data[self.name] = self.default
            with open(Path, "w", encoding="UTF-8") as file:
                file.write(json.dumps(data))
            self.value = self.default
        return self.value
    
    def __set__(self, __instance, __value):
        if not Path:
            print("[WARNING]: class", str(self) + ", connot set", __value, "because Path = None")
            return None
        with open(Path, encoding="UTF-8") as file:
            data = json.load(file)
        data[self.name] = __value
        with open(Path, "w", encoding="UTF-8") as file:
            file.write(json.dumps(data))
        self.value = __value


class SettingsData(Data):
    is_init = BooleanProperty(False)
    
    def init_with_user_data_dir(self, user_data_dir):
        data = None
        # Récupère les enciennes données si elles n'ont pas encore étés migrés
        if 'ANDROID_ARGUMENT' in os.environ:
            if os.path.exists(os.path.join(user_data_dir, '.cubis')):
                with open(os.path.join(os.path.join(user_data_dir, '.cubis'), self.file), 'r', encoding="UTF-8") as file:
                    data = file.read()
        path = user_data_dir
        # Si le fichier n'exite pas, on le créé et on copy les data de base
        if not os.path.exists(os.path.join(path, self.file)):
            with open(os.path.join(path, self.file), 'w', encoding="UTF-8") as file:
                # Migre les anciennes données si il y en a
                if data:
                    file.write(data)
                    # Supprime l'ancien dossier de data avec les fichiers s'y trouvant à l'interrieur 
                    shutil.rmtree(os.path.join(user_data_dir, '.cubis'))
                else:
                    file.write('{}')
        self.relative_path = path
        
        # ----- Set Path -----
        global Path
        Path = os.path.join(self.relative_path, self.file)
        
        # ----- Debug -----
        app = App.get_running_app()
        if app.debug:
            self.nb_hint = 3
            self.current_level = 1
        
        # ----- Call other func of other class -----
        self.is_init = True
    
    @property
    def path(self):
        return os.path.join(self.relative_path, self.file)
    
    
    
    """ ----------------------- List of properties in settings.py file ----------------------- """
    
    best_score = setting_propertie("Best_score", [0, 0, 0, 0, 0])
    last_score = setting_propertie("Last_score", 0)
    current_level = setting_propertie("Current_level", 1)
    music = setting_propertie("Music", 50)
    effect = setting_propertie("Effect", 50)
    lang = setting_propertie("lang", "en")
    fps = setting_propertie("fps", 30)
    easter_egg = setting_propertie("Easter_egg", False)
    nb_hint = setting_propertie("Nb_hint", 3)
    next_hint_time = setting_propertie("Next_hint_time", None)


Settings = SettingsData(file='settings.json')