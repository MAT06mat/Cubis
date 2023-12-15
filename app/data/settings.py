import shutil
import json
import os

from kivy.properties import BooleanProperty

from data.data import Data

class SettingsData(Data):
    is_init = BooleanProperty(False)
    __best_score = None
    __last_score = None
    __current_level = None
    __music = None
    __effect = None
    __lang = None
    __fps = None
    
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
                    file.write('{"Best_score": [0, 0, 0, 0, 0], "Last_score": 0, "Current_level": 1, "Music": 50, "Effect": 50, "lang": "en", "fps": 30}')
        self.path = path
        # Add fps = 30 in settings if not fps in settings
        self.is_init = True
    
    def get_path(self):
        return os.path.join(self.path, self.file)
    
    def __get(self, key, default):
        data = self.get()
        if key in data:
            return data[key]
        data[key] = default
        with open(self.get_path(), "w", encoding="UTF-8") as file:
            file.write(json.dumps(data))
        return default
    
    def __set(self, key, value):
        data = self.get()
        data[key] = value
        with open(self.get_path(), "w", encoding="UTF-8") as file:
            file.write(json.dumps(data))
    
    # Best_score property
    def __get_best_score(self):
        if not self.__best_score:
            self.__best_score = self.__get("Best_score", [0, 0, 0, 0, 0])
        return self.__best_score
    
    def __set_best_score(self, value):
        self.__set("Best_score", value)
        self.__best_score = value
    
    best_score = property(__get_best_score, __set_best_score)

    # Last_score property
    def __get_last_score(self):
        if not self.__last_score:
            self.__last_score = self.__get("Last_score", 0)
        return self.__last_score
    
    def __set_last_score(self, value):
        self.__set("Last_score", value)
        self.__last_score = value
    
    last_score = property(__get_last_score, __set_last_score)

    # Current_level property
    def __get_current_level(self):
        if not self.__current_level:
            self.__current_level = self.__get("Current_level", 1)
        return self.__current_level
    
    def __set_current_level(self, value):
        self.__set("Current_level", value)
        self.__current_level = value
    
    current_level = property(__get_current_level, __set_current_level)

    # Music property
    def __get_music(self):
        if not self.__music:
            self.__music = self.__get("Music", 50)
        return self.__music
    
    def __set_music(self, value):
        self.__set("Music", value)
        self.__music = value
    
    music = property(__get_music, __set_music)

    # Effect property
    def __get_effect(self):
        if not self.__effect:
            self.__effect = self.__get("Effect", 50)
        return self.__effect
    
    def __set_effect(self, value):
        self.__set("Effect", value)
        self.__effect = value
    
    effect = property(__get_effect, __set_effect)
    
    # lang property
    def __get_lang(self):
        if not self.__lang:
            self.__lang = self.__get("lang", "en")
        return self.__lang
    
    def __set_lang(self, value):
        self.__set("lang", value)
        self.__lang = value
    
    lang = property(__get_lang, __set_lang)
    
    # fps property
    def __get_fps(self):
        if not self.__fps:
            self.__fps = self.__get("fps", 30)
        return self.__fps
    
    def __set_fps(self, value):
        self.__set("fps", value)
        self.__fps = value
    
    fps = property(__get_fps, __set_fps)


Settings = SettingsData(file='settings.json')