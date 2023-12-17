"""def display_grid(grid):
    for y in grid:
        for x in y:
            if x == "NV":
                print("◻️", end=" ")
            elif x[0] == "B":
                print("❌", end=" ")
        print()

nb_cols = int(input("Combien de colones : "))
nb_raws = int(input("Combien de lines : "))

grid = []
for y in range(nb_raws):
    grid.append([])
    for x  in range(nb_cols):
        grid[y].append("NV")

display_grid(grid)"""

from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics.vertex_instructions import Line, Rectangle
from kivy.graphics import Color
import json


COLOR = ((0.65, 0.65, 0.65), (1, 0, 0), (0, 0, 1), (0, 1, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1))


def get_min_x(self):
    return self.width/2-self.size_line_h/2
def get_max_x(self):
    return self.width/2+self.size_line_h/2
def get_min_y(self):
    return self.height/2-self.size_line_v/2
def get_max_y(self):
    return self.height/2+self.size_line_v/2

class Loop:
    def __init__(self) -> None:
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        pass

def line_size_calculation(self):
    if self.nb_l >= self.nb_c:
        self.size_line = self.height/self.nb_l
        self.size_line_v = self.height
        self.size_line_h = self.size_line*self.nb_c
    else:
        self.size_line = self.width/self.nb_c
        self.size_line_v = self.size_line*self.nb_l
        self.size_line_h = self.width

def dispaly_grid(self, background=False, border=False, relative=False, animation=False):
    self.canvas.clear()
    with self.canvas:
        if background:
            Color(1, 1, 1)
            self.background_debug = Rectangle(pos=(0, 0), size=(self.width, self.height)) 
        Color(0.91, 0.72, 0.27)
        # Line Size Calculation
        line_size_calculation(self)
        if border:
            # Create cols
            for i in range(self.nb_c + 1):
                Line(points=(get_min_x(self)+i*self.size_line, get_min_y(self), get_min_x(self)+i*self.size_line, get_max_y(self)), width=2)
            # Create rows
            for i in range(self.nb_l + 1):
                Line(points=(get_min_x(self), get_min_y(self)+i*self.size_line, get_max_x(self), get_min_y(self)+i*self.size_line), width=2)
        # Create block in the grid
        rel_x = self.x
        rel_y = self.y
        if relative:
            rel_x, rel_y = 0, 0
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                block = ""
                color = (1, 1, 1)
                opacity = 1
                match self.grid[y][x][0]:
                    case "M":
                        opacity = 0.5
                    case "H":
                        block = "2"
                match self.grid[y][x][1]:
                    case "0" | "1" | "2" | "3" | "4" | "5" | "6" :
                        color = COLOR[int(self.grid[y][x][1])]
                    case "V":
                        opacity = 0
                Color(*color, opacity)
                Rectangle(pos=(rel_x+get_min_x(self)+x*self.size_line,rel_y+get_max_y(self)-(y+1)*self.size_line), size=(self.size_line, self.size_line), source=f"images/block{block}.png")
                if self.grid[y][x][0] == "B":
                    Color(1, 1, 1, 1)
                    Rectangle(pos=(rel_x+get_min_x(self)+x*self.size_line,rel_y+get_max_y(self)-(y+1)*self.size_line), size=(self.size_line, self.size_line), source=f"images/box.png")
    if background and not relative:
        self.background_debug.size = (self.width, self.height)
        self.background_debug.pos = self.pos
    elif background and relative:
        self.background_debug.size = (self.width, self.height)

def generate_grid(self, nb_cols, nb_raws):
    self.nb_l, self.nb_c = nb_raws, nb_cols
    grid = []
    for y in range(nb_raws):
        grid.append([])
        for x  in range(nb_cols):
            grid[y].append("NV")
    return grid

class Grid(RelativeLayout, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.block_text = ""
        self.type = "NV"
        self.box = ""
        self.init()
    
    def init(self):
        with open("output.json", "r") as file:
            try:
                data = json.loads(file.read())
                self.grid = data["1"]["Grid"]
            except:
                self.grid = generate_grid(self, 4, 4)
        self.nb_l = len(self.grid)
        self.nb_c = len(self.grid[0])
        self.size_hint = (1, None)
    
    def loop(self, *args):
        # Change la pos et la size du RelativeLayout
        self.height = self.width
        dispaly_grid(self=self, background=True, border=True, relative=True, animation=True)

    def new_grid(self, c="", l=""):
        if c == "":
            c = self.nb_c
        if l == "":
            l = self.nb_l
        self.grid = generate_grid(self, nb_cols=int(c), nb_raws=int(l))
    
    def change_block_text(self, text):
        self.block_text = text
    
    def change_block(self, type):
        self.type = type
    
    def change_block2(self):
        n = self.block_text.split(" ")
        self.grid[int(n[1])-1][int(n[0])-1] = self.box + self.type
    
    def change_box(self, state):
        if state == "down":
            self.box = "B"
        else:
            self.box = ""


class BlockButton(Button, Loop):
    def __init__(self, type, **kwargs):
        super().__init__(**kwargs)
        self.type = type
        self.nb_l = 1
        self.nb_c = 1
        self.grid = [[type]]
    
    def loop(self, *args):
        self.height = self.width
        dispaly_grid(self=self, background=True, border=False, relative=False, animation=False)


class GridButtons(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.orientation = "bt-lr" <-- Marche pas
        self.cols = 5
        self.bnt_list = [BlockButton(type="NV"), BlockButton(type="N1"), BlockButton(type="N2"), BlockButton(type="N3"), BlockButton(type="N4"), BlockButton(type="N5"), BlockButton(type="N6"), BlockButton(type="H0"), BlockButton(type="M1"), BlockButton(type="M2"), BlockButton(type="M3"), BlockButton(type="M4"), BlockButton(type="M5"), BlockButton(type="M6")]
        for bnt in self.bnt_list:
            self.add_widget(bnt)


class PanelRight(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid_button = GridButtons()
        self.toggle = ToggleBox()
        self.add_widget(self.grid_button)
        self.add_widget(self.toggle)


class PanelLeft(BoxLayout):
    pass


class ToggleBox(ToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Box"
    
    def on_press(self):
        self.parent.parent.grid.change_box(self.state)
        return super().on_press()


class MyScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid = Grid()
        self.panel_left = PanelLeft()
        self.panel_right = PanelRight()
        self.add_widget(self.panel_left)
        self.add_widget(self.grid)
        self.add_widget(self.panel_right)
    
    def output(self):
        with open("output.json", "w") as file:
            data = {"1": {"Grid": self.grid.grid, "Pieces": []}}
            file.write(json.dumps(data))
    
    def load(self):
        self.grid.init()


class CubisAddApp(App):
    icon = "assets/images/app/logo.png"


CubisAddApp().run()
