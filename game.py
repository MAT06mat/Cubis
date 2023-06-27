from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics.vertex_instructions import Line, Rectangle
from kivy.graphics import Color
from kivy.metrics import dp

import json

Builder.load_file("game.kv")
COLOR = ((0.65, 0.65, 0.65), (1, 0, 0), (0, 0, 1), (0, 1, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1))
def get_min_x(self):
        return self.width/2-self.size_line_h/2
def get_max_x(self):
    return self.width/2+self.size_line_h/2
def get_min_y(self):
    return self.height/2-self.size_line_v/2
def get_max_y(self):
    return self.height/2+self.size_line_v/2

def dispaly_grid(self, background=False, border=False, relative=False):
    self.canvas.clear()
    with self.canvas:
        if background:
            Color(1, 1, 1)
            self.background_debug = Rectangle(pos=(0, 0), size=(self.width, self.width)) 
        Color(0.91, 0.72, 0.27)
        # Line Size Calculation
        if self.nb_l >= self.nb_c:
            self.size_line = self.width/self.nb_l
            self.size_line_v = self.width
            self.size_line_h = self.size_line*self.nb_c
        else:
            self.size_line = self.width/self.nb_c
            self.size_line_v = self.size_line*self.nb_l
            self.size_line_h = self.width
        if border:
            # Create cols
            for i in range(self.nb_c + 1):
                Line(points=(get_min_x(self)+i*self.size_line, get_min_y(self), get_min_x(self)+i*self.size_line, get_max_y(self)), width=2)
            # Create rows
            for i in range(self.nb_l + 1):
                Line(points=(get_min_x(self), get_min_y(self)+i*self.size_line, get_max_x(self), get_min_y(self)+i*self.size_line), width=2)
        # Create block in the grid
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] != None:
                    if type(self.grid[y][x]) == str:
                        Color(*COLOR[int(self.grid[y][x])], 0.5)
                    else:
                        Color(*COLOR[int(self.grid[y][x])])
                    if not relative:
                        Rectangle(pos=(self.x+get_min_x(self)+x*self.size_line,self.y+get_max_y(self)-(y+1)*self.size_line), size=(self.size_line, self.size_line), source="images/elements/bloc.png")
                    else:
                        Rectangle(pos=(get_min_x(self)+x*self.size_line,get_max_y(self)-(y+1)*self.size_line), size=(self.size_line, self.size_line), source="images/elements/bloc.png")
        if border:
            self.background_debug.size = (self.width, self.width)


class Grid(RelativeLayout):
    def __init__(self, level, **kwargs):
        super().__init__(**kwargs)
        self.grid = level["Grid"]
        self.nb_l = len(self.grid)
        self.nb_c = len(self.grid[0])
        self.pieces = level["Pieces"]
        self.size_hint = (None, None) 
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        # Change la pos et la size du RelativeLayout
        self.width = self.parent.grid_image.width * 0.75
        self.height = self.width
        self.center_x = self.parent.grid_image.center_x
        self.center_y = self.parent.grid_image.center_y
        dispaly_grid(self=self, background=True, border=True, relative=True)

class Page(FloatLayout):
    def __init__(self, arrows, id_level, **kwargs):
        super().__init__(**kwargs)
        if arrows:
            self.add_widget(RightArrow())
            self.add_widget(LeftArrow())
        with open("levels.json") as data:
            levels = json.loads(data.read())
        self.level = levels[str(id_level)]
        self.grid_image = GridImage()
        self.add_widget(self.grid_image)
        self.grid = Grid(self.level)
        self.add_widget(self.grid)
        self.zone_piece = ZonePieces(level=self.level)
        self.add_widget(self.zone_piece)
        self.current_piece = None
    
    def change_current_piece(self, grid):
        if self.current_piece != None:
            self.remove_widget(self.current_piece)
        self.current_piece = CurrentPiece(grid)
        self.add_widget(self.current_piece)


class CurrentPiece(RelativeLayout):
    def __init__(self, grid, **kw):
        super().__init__(**kw)
        self.grid = grid
        self.nb_l = len(self.grid)
        self.nb_c = len(self.grid[0])
        self.schedule_id = Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        dispaly_grid(self, relative=True)


class MenuButton(Button):
    pass


class Arrow(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, 0.12)
        self.width = self.height
        self.schedule_id = Clock.schedule_interval(self.resize, 1/60)
    
    def resize(self, *args):
        self.width = self.height
        self.y = self.parent.grid_image.y - self.height/1.2


class MyScrollView(ScrollView):
    def __init__(self, current_level, **kwargs):
        super().__init__(**kwargs)
        self.current_level = current_level
        self.grid_piece = GridPiece(current_level=self.current_level)
        self.add_widget(self.grid_piece)


class RightArrow(Arrow):
    pass


class LeftArrow(Arrow):
    pass


class GridImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {"center_x": 0.5, "top": 0.94}
        self.size_hint = (None, None)
        self.fit_mode = "contain"
        self.source = "images/elements/grid.png"
        self.on_window_resize()
        Window.bind(on_resize=self.on_window_resize)
    
    def on_window_resize(self, *args):
        self.width = Window.width
        self.height = self.width
        while self.height > 0.6 * Window.height:
            self.height -= 1
        while self.width > self.height:
            self.width -= 1


class PieceButton(Button):
    def __init__(self, piece,**kwargs):
        super().__init__(**kwargs)
        self.piece = piece
        self.grid = self.piece["Grid"]
        self.nb_l = len(self.grid)
        self.nb_c = len(self.grid[0])
        self.size_hint_y = None
        Clock.schedule_interval(self.resize, 1/60)
    
    def on_press(self):
        self.parent.parent.parent.parent.change_current_piece(grid=self.grid)
        return super().on_press()
    
    def resize(self, *args):
        self.height = self.width
        dispaly_grid(self)

class GridPiece(GridLayout):
    def __init__(self, current_level, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.spacing = dp(10)
        self.current_level = current_level
        for piece in self.current_level["Pieces"]:
            self.add_widget(PieceButton(piece=piece))


class ZonePieces(BoxLayout):
    def __init__(self, level, **kwargs):
        super().__init__(**kwargs)
        self.level = level
        self.my_scroll_view = MyScrollView(current_level=level)
        self.add_widget(self.my_scroll_view)
        Clock.schedule_interval(self.resize, 1/60)
    
    def resize(self, *args):
        self.height = self.parent.height - self.parent.grid_image.height - 0.15*self.parent.height


class Game(Screen):
    def __init__(self, id_level, **kw):
        super().__init__(**kw)
        self.id_level = id_level
        self.level_name = "Niveau " + str(id_level)
        with open("data.json", "r") as data:
            data_open = json.loads(data.read())
        for area in data_open["Areas"]:
            for level in area["Levels"]:
                if level["Id"] == id_level:
                    self.mode = level["Mode"]
                    self.background = area["Background"]
        self.arrows = "Rotation" in self.mode
        self.my_float = FloatLayout()
        self.my_float.add_widget(Image(source=self.background, fit_mode="cover"))
        self.my_float.add_widget(Page(arrows=self.arrows, id_level=id_level))
        self.add_widget(self.my_float)
        