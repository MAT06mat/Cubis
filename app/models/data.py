import json


class Data:
    path = "data/"
    path_rel = None
    
    def get(self, key: str):
        key = str(key)
        with open(self.path+self.path_rel) as file:
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
                with open(self.path+self.path_rel) as file:
                    data = json.load(file)
                data[key] = element
            except KeyError:
                return KeyError
        with open(self.path+self.path_rel, "w") as file:
            file.write(json.dumps(data))


class SettingsData(Data):
    path_rel = "settings.json"


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