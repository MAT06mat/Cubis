from data.data import Data


class LevelsData(Data):
    def get(self, value=None):
        return super().get(str(value))


Levels = LevelsData(file='levels.json')