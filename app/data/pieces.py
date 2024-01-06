import random
import copy

from data.data import Data
from models.grid_calculation import symmetry, turn


class PiecesData(Data):
    def __init__(self, file):
        super().__init__(file)
        self.init()
    
    def init(self):
        self.pieces_list = self.get()
        self.increase_int = 0
    
    def random_piece(self):
        population = []
        weights = []
        for piece in self.pieces_list:
            if piece["Proba"] >= 1:
                population.append(piece["Piece"])
                weights.append(piece["Proba"])
        # Choose a random piece
        random_piece = copy.deepcopy(random.choices(population=population, weights=weights)[0])
        # Choose a random color
        color = random.choice(["N1", "N2", "N3", "N4", "N5", "N6"])
        for y in range(len(random_piece)):
            for x  in range(len(random_piece[y])):
                if random_piece[y][x] != "NV":
                    random_piece[y][x] = color
        # Choose a random translation
        if random.random() < 0.5:
            random_piece = turn(random_piece, random.random() < 0.5)
        if random.random() < 0.5:
            random_piece = symmetry(random_piece)
        if random.random() < 0.5:
            random_piece = symmetry(random_piece, vertical=False)
        return random_piece
    
    def increase(self):
        self.increase_int += 1
        for piece in self.pieces_list[::-1]:
            if piece["Proba"] < 100:
                piece["Proba"] *= 1.09
            else:
                piece["Proba"] *= 1.04


Pieces = PiecesData(file='pieces.json')