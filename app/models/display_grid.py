from kivy.graphics.vertex_instructions import Line, Rectangle
from kivy.graphics import Color

from models.grid_calculation import GridCalculation

COLOR = ((0.65, 0.65, 0.65), (1, 0, 0), (0, 0, 1), (0, 1, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1))
ANIMATION_LIST = []


class DisplayGrid(GridCalculation):
    def display_grid(self, background=False, border=False, relative=False, animation=False, border_block=False, reload=True, angle=0) -> None:
        """Display the grid with parameters"""
        self.canvas.clear()
        if not reload:
            return
        with self.canvas:
            if background:
                Color(1, 1, 1)
                self.background_debug = Rectangle(pos=(0, 0), size=(self.width, self.height)) 
            Color(0.91, 0.72, 0.27)
            # Line Size Calculation
            self.line_size_calculation()
            if border:
                # Create cols
                for i in range(len(self.grid[0]) + 1):
                    Line(points=(self.min_x+i*self.size_line, self.min_y, self.min_x+i*self.size_line, self.max_y), width=2)
                # Create rows
                for i in range(len(self.grid) + 1):
                    Line(points=(self.min_x, self.min_y+i*self.size_line, self.max_x, self.min_y+i*self.size_line), width=2)
            # Create block in the grid
            rel_x = self.x
            rel_y = self.y
            if relative:
                rel_x, rel_y = 0, 0
            for y in range(len(self.grid)):
                for x in range(len(self.grid[y])):
                    block = "block"
                    color = (1, 1, 1)
                    opacity = 1
                    c_1 = self.grid[y][x][1]
                    if c_1 == "0" or c_1 == "1" or c_1 == "2" or c_1 == "3" or c_1 == "4" or c_1 == "5" or c_1 == "6":
                        color = COLOR[int(self.grid[y][x][1])]
                    elif c_1 == "V":
                        opacity = 0
                    c_0 = self.grid[y][x][0]
                    if c_0 ==  "M":
                        opacity = 0.5
                    elif c_0 == "H":
                        block = "hard_block"
                    elif c_0 == "B":
                        color = (1, 1, 1)
                        block = "box"
                    elif c_0 == "T":
                        color = (1, 1, 1)
                        block = "hole"
                        opacity = 1
                    rotation = 0
                    if angle != 0:
                        if 91 > angle > 0:
                            rotation = 90
                        elif 181 > angle > 90:
                            rotation = 180
                        elif 271 > angle > 180:
                            rotation = 270
                        elif -91 < angle < 0:
                            rotation = -90
                        elif -181 < angle < -90:
                            rotation = -180
                        elif -271 < angle < -180:
                            rotation = -270
                    Color(*color, opacity)
                    Rectangle(pos=(rel_x+self.min_x+x*self.size_line,rel_y+self.max_y-(y+1)*self.size_line), size=(self.size_line, self.size_line), source=f"assets/images/elements/{block}/0.png")
                    if angle != 0:
                        Color(*color, abs(opacity*angle/90))
                        Rectangle(pos=(rel_x+self.min_x+x*self.size_line,rel_y+self.max_y-(y+1)*self.size_line), size=(self.size_line, self.size_line), source=f"assets/images/elements/{block}/{rotation}.png")
            if border_block:
                border_block_width = 1.5
                Color(0.91, 0.72, 0.27, 1)
                for y in range(len(self.grid)):
                    for x in range(len(self.grid[y])):
                        if self.grid_id[y][x] == None:
                            continue
                        # Side left
                        if x == 0:
                            Line(points=(self.min_x+x*self.size_line+1, self.max_y-y*self.size_line, self.min_x+x*self.size_line+1, self.max_y-(y+1)*self.size_line), width=border_block_width)
                        else: 
                            if self.grid_id[y][x] != self.grid_id[y][x-1]:
                                Line(points=(self.min_x+x*self.size_line+1, self.max_y-y*self.size_line, self.min_x+x*self.size_line+1, self.max_y-(y+1)*self.size_line), width=border_block_width)
                        # Side top
                        if y == 0:
                            Line(points=(self.min_x+x*self.size_line, self.max_y-y*self.size_line-1, self.min_x+(x+1)*self.size_line, self.max_y-y*self.size_line-1), width=border_block_width)
                        else: 
                            if self.grid_id[y][x] != self.grid_id[y-1][x]:
                                Line(points=(self.min_x+x*self.size_line, self.max_y-y*self.size_line-1, self.min_x+(x+1)*self.size_line, self.max_y-y*self.size_line-1), width=border_block_width)
                        # Side right
                        if x+1 == len(self.grid[y]):
                            Line(points=(self.min_x+(x+1)*self.size_line-1, self.max_y-y*self.size_line, self.min_x+(x+1)*self.size_line-1, self.max_y-(y+1)*self.size_line), width=border_block_width)
                        else: 
                            if self.grid_id[y][x] != self.grid_id[y][x+1]:
                                Line(points=(self.min_x+(x+1)*self.size_line-1, self.max_y-y*self.size_line, self.min_x+(x+1)*self.size_line-1, self.max_y-(y+1)*self.size_line), width=border_block_width)
                        # Side bottom
                        if y+1 == len(self.grid):
                            Line(points=(self.min_x+x*self.size_line, self.max_y-(y+1)*self.size_line+1, self.min_x+(x+1)*self.size_line, self.max_y-(y+1)*self.size_line+1), width=border_block_width)
                        else: 
                            if self.grid_id[y][x] != self.grid_id[y+1][x]:
                                Line(points=(self.min_x+x*self.size_line, self.max_y-(y+1)*self.size_line+1, self.min_x+(x+1)*self.size_line, self.max_y-(y+1)*self.size_line+1), width=border_block_width)
                Color(0.94, 0.77, 1.0, 1)
                hint_border_width = 3
                for y in range(len(self.grid)):
                    for x in range(len(self.grid[y])):
                        if self.grid_hint_id[y][x] == None:
                            continue
                        # Side left
                        if x == 0:
                            Line(points=(self.min_x+x*self.size_line, self.max_y-y*self.size_line, self.min_x+x*self.size_line, self.max_y-(y+1)*self.size_line), width=hint_border_width)
                        else: 
                            if self.grid_hint_id[y][x] != self.grid_hint_id[y][x-1]:
                                Line(points=(self.min_x+x*self.size_line, self.max_y-y*self.size_line, self.min_x+x*self.size_line, self.max_y-(y+1)*self.size_line), width=hint_border_width)
                        # Side top
                        if y == 0:
                            Line(points=(self.min_x+x*self.size_line, self.max_y-y*self.size_line, self.min_x+(x+1)*self.size_line, self.max_y-y*self.size_line), width=hint_border_width)
                        else: 
                            if self.grid_hint_id[y][x] != self.grid_hint_id[y-1][x]:
                                Line(points=(self.min_x+x*self.size_line, self.max_y-y*self.size_line, self.min_x+(x+1)*self.size_line, self.max_y-y*self.size_line), width=hint_border_width)
                        # Side right
                        if x+1 == len(self.grid[y]):
                            Line(points=(self.min_x+(x+1)*self.size_line, self.max_y-y*self.size_line, self.min_x+(x+1)*self.size_line, self.max_y-(y+1)*self.size_line), width=hint_border_width)
                        else: 
                            if self.grid_hint_id[y][x] != self.grid_hint_id[y][x+1]:
                                Line(points=(self.min_x+(x+1)*self.size_line, self.max_y-y*self.size_line, self.min_x+(x+1)*self.size_line, self.max_y-(y+1)*self.size_line), width=hint_border_width)
                        # Side bottom
                        if y+1 == len(self.grid):
                            Line(points=(self.min_x+x*self.size_line, self.max_y-(y+1)*self.size_line, self.min_x+(x+1)*self.size_line, self.max_y-(y+1)*self.size_line), width=hint_border_width)
                        else: 
                            if self.grid_hint_id[y][x] != self.grid_hint_id[y+1][x]:
                                Line(points=(self.min_x+x*self.size_line, self.max_y-(y+1)*self.size_line, self.min_x+(x+1)*self.size_line, self.max_y-(y+1)*self.size_line), width=hint_border_width)
            if animation:
                for animation in ANIMATION_LIST:
                    if animation.type == "box":
                        # Add object
                        Color(1, 1, 1, animation.object_opacity/100)
                        Rectangle(pos=animation.animation_pos, size=animation.animation_size, source=animation.object)
                        # Add animation
                        Color(1, 1, 1, 1)
                        Rectangle(pos=animation.animation_pos, size=animation.animation_size, source=animation.current_frame)
                    elif animation.type == "Hole":
                        Color(*COLOR[int(animation.color)], animation.opacity)
                        Rectangle(pos=animation.animation_pos, size=(self.size_line, self.size_line), source="assets/images/elements/block/0.png")
                        if animation.opacity == None:
                            ANIMATION_LIST.remove(animation)
                            animation.reload = False
                    elif animation.type == "Hint":
                        Color(0.96, 0.9, 1, animation.opacity)
                        Rectangle(pos=animation.animation_pos, size=(self.size_line, self.size_line), source="assets/images/elements/hint/0.png")
                        if animation.opacity == 0:
                            ANIMATION_LIST.remove(animation)
                            animation.reload = False
        if background and not relative:
            self.background_debug.size = (self.width, self.height)
            self.background_debug.pos = self.pos
        elif background and relative:
            self.background_debug.size = (self.width, self.height)


"""
B__ : "Box"
N_ : "Normal"
M_ : "Motif"
H_ : "Hard Block"
T_ : "Hole" (Trou)
_V : "Void"
_0 : "Color 0"
_1 : "Color 1"
_2 : "Color 2"
_3 : "Color 3"
_4 : "Color 4"
_5 : "Color 5"
_6 : "Color 6"
Possibilities :
- NV
- N5
- M5
- H0
- BNV
- BH0
- BM5
- TV
"""