import random


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

def turn(grid, right=True) -> list:
    new_grid = [["NV" for x in grid] for y in grid[0]]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if right:
                new_grid[x][-(y+1)] = grid[y][x]
            else:
                new_grid[-(x+1)][y] = grid[y][x]
    return new_grid

def symmetry(grid, vertical=True):
    new_grid = [["NV" for x in grid[0]] for y in grid]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if vertical:
                new_grid[y][x] = grid[y][-(x+1)]
            else:
                new_grid[y][x] = grid[-(y+1)][x]
    return new_grid

def random_grid(size, nb):
    grid = generate_grid(size=size)
    if nb <= 50:
        return grid
    types_grid = []
    chance = 0
    # Append type of grid that be used
    if nb > 50:
        types_grid.append(["H0"])
        chance += 10
    if nb > 90:
        types_grid.append(["MC"])
    if nb > 130:
        types_grid.append(["H0", "MC"])
        chance += 10
    if nb > 180:
        types_grid.append(["TV"])
    if nb > 240:
        types_grid.append(["BH0"])
        chance += 5
    if nb > 300:
        types_grid.append(["BNV", "BH0"])
        chance += 3
    if nb > 350:
        types_grid.append(["H0", "BNV", "BH0"])
    if nb > 400:
        types_grid.append(["MC", "TV"])
        chance += 2
    # Choose a random type of grid
    try:
        type_grid = random.choice(types_grid)
    except:
        return grid
    # Choose a random interger of point in grid
    nb_point = random.randint(0, 30)
    if nb_point > chance:
        return grid
    a = size**2
    # Append a absolu index of points in grid
    point_list = []
    for i in range(0, random.randint(int(nb_point/100*a), int(nb_point/60*a))):
        point_list.append(random.randint(0, a))
    index = 0
    # Add in grid the points
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            index += 1
            if index in point_list:
                grid[y][x] = random.choice(type_grid)
    # Choose random color
    colors = random.choices(population=["1", "2", "3", "4", "5", "6"], k=random.choice([2, 3, 4]))
    # Color the block can be colored
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x][-1] == "C":
                grid[y][x] = grid[y][x][:-1]
                grid[y][x] = grid[y][x] + random.choice(colors)
    return grid