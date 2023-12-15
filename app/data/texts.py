from kivy.properties import StringProperty

from data.data import Data
from data.settings import Settings


class TextsData(Data):
    current_lang = StringProperty("en")
    
    def __init__(self, file):
        super().__init__(file)
        Settings.bind(is_init=self.setting_change)
        self.lang_dict = {"en": "English", "fr": "Français"}
    
    def setting_change(self, *args):
        try:
            self.current_lang = Settings.lang
        except:
            Settings.lang = "en"
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
    
    def complete_lang(self, lang):
        if lang in self.lang_dict:
            return self.lang_dict[lang]
        else:
            return KeyError
    
    def uncomplete_lang(self, lang):
        for key in self.lang_dict.keys():
            if key == lang.lower()[:2]:
                return key
        return KeyError


Texts = TextsData(file="traductions.json")