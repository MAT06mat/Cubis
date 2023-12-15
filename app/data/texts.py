from kivy.properties import StringProperty

from data.data import Data
from data.settings import Settings


class Traductions(Data):
    current_lang = StringProperty("en")
    
    def __init__(self, file):
        super().__init__(file)
        Settings.bind(is_init=self.init)
        self.lang_dict = {}
        traductions = self.get()
        for traduction in traductions:
            lang = traduction["lang"]
            complete_lang = traduction["complete_lang"]
            self.lang_dict[lang] = complete_lang
        #   self.lang_dict <=> {"en": "English", "fr": "Français", ...}
    
    def init(self, *args):
        self.current_lang = Settings.lang
    
    def key(self, key):
        key = str(key)
        for texts in self.get():
            if texts["lang"] == Settings.lang:
                if key in texts:
                    text = texts[key]
                    return text
                else:
                    return KeyError
    
    def change_lang(self, new_lang):
        if new_lang in self.lang_dict.keys():
            Settings.lang = new_lang
            self.current_lang = new_lang
        else:
            return KeyError

    def image_path(self, path: str):
        path = path.split(".")
        if len(path) != 2:
            return ValueError
        path = f'{path[0]}-{self.current_lang}.{path[1]}'
        return path
    
    def complete_lang(self, lang):
        return self.lang_dict[lang]
    
    def uncomplete_lang(self, lang):
        for key in self.lang_dict.keys():
            if lang == self.lang_dict[key]:
                return key
        return KeyError


Texts = Traductions(file="traductions.json")