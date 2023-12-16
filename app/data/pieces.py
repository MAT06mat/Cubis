from data.data import Data


class PiecesData(Data):
    def get(self, value=None):
        return super().get(str(value))


Pieces = PiecesData(file='pieces.json')