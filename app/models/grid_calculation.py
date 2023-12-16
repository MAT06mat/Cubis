class GridCalculation():
    @property
    def min_x(self) -> float:
        return self.width/2-self.size_line_h/2
    @property
    def max_x(self) -> float:
        return self.width/2+self.size_line_h/2
    @property
    def min_y(self) -> float:
        return self.height/2-self.size_line_v/2
    @property
    def max_y(self) -> float:
        return self.height/2+self.size_line_v/2

    def line_size_calculation(self) -> None:
        if len(self.grid) >= len(self.grid[0]):
            self.size_line = self.height/len(self.grid)
            self.size_line_v = self.height
            self.size_line_h = self.size_line*len(self.grid[0])
        else:
            self.size_line = self.width/len(self.grid[0])
            self.size_line_v = self.size_line*len(self.grid)
            self.size_line_h = self.width


def generate_grid(size=None, width=None, height=None) -> list:
    if size:
        width, height = size, size
    elif width and height:
        pass
    else:
        return ValueError
    return [["NV" for x in range(width)] for y in range(height)]

def turn(grid) -> list:
    new_grid = [["NV" for x in grid] for y in grid[0]]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            new_grid[-(x+1)][y] = grid[y][x]
    return new_grid