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

from message import MenuMessage, InfoMessage
from story_game import UndoButton, GridImage

import copy
import json
import random

Builder.load_file("infinite_game.kv")

COLOR = ((0.65, 0.65, 0.65), (1, 0, 0), (0, 0, 1), (0, 1, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1))

def define():
    with open("data.json", "r") as file:
        data = json.load(file)
        global BEST_SCORE
        global LAST_SCORE
        BEST_SCORE = data["Best_score"]
        LAST_SCORE = data["Last_score"]

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
            self.background_debug = Rectangle(pos=(0, 0), size=(self.width, self.height)) 
        Color(0.91, 0.72, 0.27)
        # Line Size Calculation
        if self.nb_l >= self.nb_c:
            self.size_line = self.height/self.nb_l
            self.size_line_v = self.height
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
        if background and not relative:
            self.background_debug.size = (self.width, self.height)
            self.background_debug.pos = self.pos
        elif background and relative:
            self.background_debug.size = (self.width, self.height)


class MenuButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        self.x = Window.width - self.width*0.9
        self.y = Window.height - self.height*0.9
    
    def on_press(self):
        if self.parent.message != None:
            return super().on_press()
        self.parent.message_push()
        return super().on_press()


class CurrentPiece(RelativeLayout):
    def __init__(self, grid, **kw):
        super().__init__(**kw)
        self.grid = grid
        self.nb_l = len(self.grid)
        self.nb_c = len(self.grid[0])
        self.size_hint = (None, None)
        self.loop(self, None)
        self.delta_pos = (self.width/2, self.height/2)
        self.pos = (Window.mouse_pos[0] - self.delta_pos[0], Window.mouse_pos[1] - self.delta_pos[1])
        Clock.schedule_interval(self.loop, 1/60)
        Window.bind(on_resize=self.on_window_resize)
    
    def loop(self, *args):
        try:
            self.size_line = self.parent.grid.size_line
        except:
            self.size_line = dp(50)
        self.width = self.nb_c*self.size_line
        self.height = self.nb_l*self.size_line
        dispaly_grid(self, relative=True)
    
    def on_touch_down(self, touch):
        if self.parent.message != None:
            return
        if self.pos[0] < touch.pos[0] < (self.pos[0] + self.width) and self.pos[1] < touch.pos[1] < (self.pos[1] + self.height):
            self.delta_pos = (touch.pos[0] - self.pos[0], touch.pos[1] - self.pos[1])
        else:
            self.delta_pos = None
    
    def on_touch_move(self, touch):
        if self.parent.message != None:
            return
        if self.delta_pos != None:
            self.pos = (touch.pos[0] - self.delta_pos[0], touch.pos[1] - self.delta_pos[1])
    
    def on_window_resize(self, *args):
        self.pos = (Window.width/2-self.width/2, Window.height/2-self.width/2)
    
    
    def right(self):
        self.new_grid = []
        for y in range(self.nb_c):
            self.new_grid.append([])
            for x in range(self.nb_l):
                self.new_grid[y].append(None)
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.new_grid[x][-(y+1)] = self.grid[y][x]
        self.grid = self.new_grid
        self.nb_l = len(self.grid)
        self.nb_c = len(self.grid[0])
    
    def left(self):
        self.new_grid = []
        for y in range(self.nb_c):
            self.new_grid.append([])
            for x in range(self.nb_l):
                self.new_grid[y].append(None)
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.new_grid[-(x+1)][y] = self.grid[y][x]
        self.grid = self.new_grid
        self.nb_l = len(self.grid)
        self.nb_c = len(self.grid[0])


class PieceButton(Button):
    def __init__(self, grid,**kwargs):
        super().__init__(**kwargs)
        self.grid = grid
        self.nb_l = len(self.grid)
        self.nb_c = len(self.grid[0])
        self.size_hint_y = None
        Clock.schedule_interval(self.loop, 1/60)
    
    def on_press(self):
        if self.parent.parent.parent.parent.message != None:
            return super().on_press()
        self.parent.parent.parent.parent.change_current_piece(grid=self.grid)
        return super().on_press()
    
    def loop(self, *args):
        self.width = (Window.width-dp(40))/3
        self.height = self.width
        dispaly_grid(self)


class GridPiece(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.piece_button = []
        for i in range(6):
            try:
                grid = self.generation(2)
            except:
                grid = [None]
            button = PieceButton(grid=grid)
            self.piece_button.append(button)
            self.add_widget(button)
    
    def generation(self, size=2):
        color = random.randint(1, 6)
        grid = []
        for y in range(size):
            grid.append([])
            for x  in range(size):
                r = random.randint(1, 100)
                if r > 35:
                    grid[y].append(color)
                else:
                    grid[y].append(None)
        grid = self.simplify(grid)
        if grid == []:
            grid = self.generation(size)
        return grid

    def simplify(self, grid):
        operation = 0
        top = []
        try:
            for x in grid[0]:
                top.append(x != None)
            if not any(top):
                grid.pop(0)
                operation = 1
        except:
            pass
        bottom = []
        try:
            for x in grid[-1]:
                bottom.append(x != None)
            if not any(bottom):
                grid.pop(-1)
                operation = 1
        except:
            pass
        left = []
        try:
            for y in grid:
                left.append(y[0] != None)
            if not any(left):
                for y in grid:
                    y.pop(0)
                operation = 1
        except:
            pass
        right = []
        try:
            for y in grid:
                right.append(y[-1] != None)
            if not any(right):
                for y in grid:
                    y.pop(-1)
                operation = 1
        except:
            pass
        if operation == 1:
            grid = self.simplify(grid)
        return grid


class MyScrollView(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid_piece = GridPiece()
        self.add_widget(self.grid_piece)
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        self.disabled = self.parent.parent.message != None


class ZonePieces(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.my_scroll_view = MyScrollView()
        self.add_widget(self.my_scroll_view)
        Clock.schedule_interval(self.resize, 1/60)
    
    def resize(self, *args):
        self.height = self.parent.height - self.parent.grid_image.height - 0.15*self.parent.height


class InfiniteGrid(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
        self.nb_l = 4
        self.nb_c = 4
        self.size_hint = (None, None)
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        # Change la pos et la size du RelativeLayout
        self.width = self.parent.grid_image.width * 0.75
        self.height = self.width
        self.center_x = self.parent.grid_image.center_x
        self.center_y = self.parent.grid_image.center_y
        dispaly_grid(self=self, background=True, border=True, relative=True)


class Arrow(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.resize, 1/60)
    
    def resize(self, *args):
        self.width = self.height
        self.y = self.parent.grid_image.y - self.height/1.2


class RightArrow(Arrow):
    def on_press(self):
        if self.parent.message != None:
            return super().on_press()
        self.parent.right()
        return super().on_press()


class LeftArrow(Arrow):
    def on_press(self):
        if self.parent.message != None:
            return super().on_press()
        self.parent.left()
        return super().on_press()


class InfinitePage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_piece = None
        self.message = None
        self.mouse_pos = None
        self.can_place = False
        self.saves = []
        self.add_widget(RightArrow())
        self.add_widget(LeftArrow())
        self.grid = InfiniteGrid()
        self.zone_piece = ZonePieces()
        self.undo_button = UndoButton()
        self.grid_image = GridImage()
        self.add_widget(self.grid_image)
        self.add_widget(self.grid)
        self.add_widget(self.zone_piece)
        self.add_widget(self.undo_button)
        if BEST_SCORE[0] == 0:
            print("Bonjour")
            self.message = InfoMessage(message=("Bienvenue dans le\n mode infini de Cubis !", "Dans ce mode,\nle but est de remplir le\nplus possible de grilles.", "Vous aurez à chaque fois\n6 pièces pour la remplir.","A chaque pièce posé,\nvous en regagnerez une autre.", "Le but est donc de faire\nle meilleur score possible.", "Vous avez le droit de tourner\nles pièces autant de fois\nque vous le souhaitez.", "Bonne chance !"))
            self.add_widget(self.message)
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        self.undo_button.disabled = not (len(self.saves) >= 1 or self.current_piece != None)
        self.verify()
        for y in self.grid.grid:
            for x in y:
                if type(x) != int:
                    return
        self.grid.grid = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
    
    def on_touch_up(self, touch):
        if self.message:
            return
        self.verify()
        if self.can_place:
            self.can_place = False
            self.save()
            self.marg = int(self.grid.size_line/2)
            for y_p in range(len(self.current_piece.grid)):
                for x_p in range(len(self.current_piece.grid[y_p])):
                    if self.current_piece.grid[y_p][x_p] != None:
                        for y_g in range(len(self.grid.grid)):
                            for x_g in range(len(self.grid.grid[y_g])):
                                # Calculation Global of x and y for piece and grid
                                x_piece = get_min_x(self.current_piece)+self.current_piece.x+x_p*self.current_piece.size_line
                                y_piece = get_max_y(self.current_piece)+self.current_piece.y-(y_p+1)*self.current_piece.size_line
                                x_grid = get_min_x(self.grid)+self.grid.x+x_g*self.grid.size_line
                                y_grid = get_max_y(self.grid)+self.grid.y-(y_g+1)*self.grid.size_line
                                # if grid block match with piece block and if is void or if is a motifs
                                if abs(x_piece - x_grid) < self.marg and abs(y_piece - y_grid) < self.marg and (self.grid.grid[y_g][x_g] == None or (self.grid.grid[y_g][x_g] == str(self.current_piece.grid[y_p][x_p]) and type(self.grid.grid[y_g][x_g]) == str)):
                                    self.grid.grid[y_g][x_g] = self.current_piece.grid[y_p][x_p]
            self.remove_widget(self.current_piece)
            piece_find = False
            while not piece_find:
                for piece in self.zone_piece.my_scroll_view.grid_piece.piece_button:
                    if piece.grid == self.current_piece.grid and not piece_find:
                        piece_find = True
                        self.zone_piece.my_scroll_view.grid_piece.piece_button.remove(piece)
                        self.zone_piece.my_scroll_view.grid_piece.remove_widget(piece)
                self.left()
            self.current_piece = None
            try:
                grid = self.zone_piece.my_scroll_view.grid_piece.generation(2)
            except:
                grid = [None]
            button = PieceButton(grid=grid)
            self.zone_piece.my_scroll_view.grid_piece.piece_button.append(button)
            self.zone_piece.my_scroll_view.grid_piece.add_widget(button)
    
    def save(self):
        grid = copy.deepcopy(self.grid.grid)
        pieces = []
        for piece in self.zone_piece.my_scroll_view.grid_piece.piece_button:
            pieces.append(piece.grid)
        self.saves.append((grid, pieces))
    
    def undo(self):
        if self.current_piece:
            self.remove_widget(self.current_piece)
            self.current_piece = None
            return
        self.grid.grid = self.saves[-1][0]
        self.zone_piece.my_scroll_view.grid_piece.piece_button = []
        self.zone_piece.my_scroll_view.grid_piece.clear_widgets()
        for piece in self.saves[-1][1]:
            button = PieceButton(grid=piece)
            self.zone_piece.my_scroll_view.grid_piece.piece_button.append(button)
            self.zone_piece.my_scroll_view.grid_piece.add_widget(button)
        self.saves.pop(-1)
    
    def change_current_piece(self, grid):
        if self.current_piece != None:
            self.remove_widget(self.current_piece)
        self.current_piece = CurrentPiece(grid)
        self.add_widget(self.current_piece)

    def message_push(self):
        if not self.message:
            self.message = MenuMessage(id_level=self.id_level, mode=self.mode)
            self.add_widget(self.message)
        
    def message_pop(self):
        if self.message:
            self.remove_widget(self.message)
            self.message = None
    
    def verify(self):
        try:
            if self.current_piece:
                self.marg = int(self.grid.size_line/2)
                check = []
                for y_p in range(len(self.current_piece.grid)):
                    for x_p in range(len(self.current_piece.grid[y_p])):
                        one = []
                        for y_g in range(len(self.grid.grid)):
                            for x_g in range(len(self.grid.grid[y_g])):
                                # Calculation Global of x and y for piece and grid
                                x_piece = get_min_x(self.current_piece)+self.current_piece.x+x_p*self.current_piece.size_line
                                y_piece = get_max_y(self.current_piece)+self.current_piece.y-(y_p+1)*self.current_piece.size_line
                                x_grid = get_min_x(self.grid)+self.grid.x+x_g*self.grid.size_line
                                y_grid = get_max_y(self.grid)+self.grid.y-(y_g+1)*self.grid.size_line
                                # if grid block match with piece block and if is void or if is a motis
                                one.append(abs(x_piece - x_grid) < self.marg and abs(y_piece - y_grid) < self.marg and (self.grid.grid[y_g][x_g] == None or (self.grid.grid[y_g][x_g] == str(self.current_piece.grid[y_p][x_p]) and type(self.grid.grid[y_g][x_g]) == str) or self.current_piece.grid[y_p][x_p] == None))
                        check.append(any(one))
                self.can_place = all(check)
        except:
            self.can_place = False

    def right(self):
        if self.current_piece != None:
            self.current_piece.right()

    def left(self):
        if self.current_piece != None:
            self.current_piece.left()


class InfiniteGame(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        define()
        self.my_float = FloatLayout()
        self.my_float.add_widget(Image(source="images/backgrounds/space.jpg", fit_mode="cover"))
        self.my_float.add_widget(InfinitePage())
        self.add_widget(self.my_float)
        