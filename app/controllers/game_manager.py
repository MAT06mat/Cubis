from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.properties import ListProperty, NumericProperty, BooleanProperty
from kivy.graphics.vertex_instructions import Line, Rectangle
from kivy.graphics import Color
from kivy.metrics import dp

from models.loop import Loop
from controllers.message import MenuMessage, InfoMessage, VictoireMessage
from models.data import SETTINGS, PIECES, AREAS, LEVELS

import os
import copy
import random

current_directory = os.path.dirname(os.path.realpath(__file__))
kv_file_path = os.path.join(current_directory, "../views/game.kv")
Builder.load_file(kv_file_path)

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
                        Rectangle(pos=(self.x+get_min_x(self)+x*self.size_line,self.y+get_max_y(self)-(y+1)*self.size_line), size=(self.size_line, self.size_line), source="../images/elements/bloc.png")
                    else:
                        Rectangle(pos=(get_min_x(self)+x*self.size_line,get_max_y(self)-(y+1)*self.size_line), size=(self.size_line, self.size_line), source="../images/elements/bloc.png")
        if background and not relative:
            self.background_debug.size = (self.width, self.height)
            self.background_debug.pos = self.pos
        elif background and relative:
            self.background_debug.size = (self.width, self.height)

def generate_grid(size):
    grid = []
    for y in range(size):
        grid.append([])
        for x  in range(size):
            grid[y].append(None)
    return grid


class RedoButton(Button, Loop):
    def loop(self, *args):
        self.x = self.width*0.8
        self.y = Window.height - self.height*0.9

    def on_press(self):
        if self.parent.message != None:
            return super().on_press()
        self.parent.redo()
        return super().on_press()


class UndoButton(Button, Loop):
    def loop(self, *args):
        self.y = Window.height - self.height*0.9

    def on_press(self):
        if self.parent.message != None:
            return super().on_press()
        self.parent.undo()
        return super().on_press()


class GridImage(Image, Loop):
    def loop(self, *args):
        self.width = Window.width
        self.height = self.width
        while self.height > 0.6 * Window.height:
            self.height -= 1
        while self.width > self.height:
            self.width -= 1


class ScoreCase(Label, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, 0.1)
        self.width = self.height
        with self.canvas.before:
            self.background_r = Rectangle(source='images/elements/score.png')
    
    def loop(self, *args):
        self.x = self.parent.menu_button.x - self.width
        self.y = Window.height - self.height*0.9
        self.background_r.size = (self.size[0], self.size[1]*0.6)
        self.background_r.pos = (self.pos[0], self.pos[1]+self.size[1]*0.2)
    

class MenuButton(Button, Loop):
    def loop(self, *args):
        self.x = Window.width - self.width*0.9
        self.y = Window.height - self.height*0.9
    
    def on_press(self):
        if self.parent.message != None:
            return super().on_press()
        self.parent.message_push()
        return super().on_press()


class CurrentPiece(RelativeLayout, Loop):
    grid = ListProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nb_l = len(self.grid)
        self.nb_c = len(self.grid[0])
        self.size_hint = (None, None)
        self.loop(self, None)
        self.delta_pos = (self.width/2, self.height/2)
        self.pos = (Window.mouse_pos[0] - self.delta_pos[0], Window.mouse_pos[1] - self.delta_pos[1])
        Window.bind(on_resize=self.on_window_resize)
    
    def loop(self, *args):
        try:
            self.size_line = self.parent.grid.size_line
        except:
            self.size_line = dp(50)
        self.width = self.nb_c*self.size_line
        self.height = self.nb_l*self.size_line
        dispaly_grid(self, relative=True)
    
    def on_window_resize(self, *args):
        self.pos = (Window.width/2-self.width/2, Window.height/2-self.width/2)
    
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


class PieceButton(Button, Loop):
    grid = ListProperty(None)
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.nb_l = len(self.grid)
        self.nb_c = len(self.grid[0])
        self.size_hint_y = None
    
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
    piece_button = ListProperty([])
    tiers = NumericProperty(3)
    piece_generated = NumericProperty(70)
    id_level = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.id_level == 0:
            for i in range(6):
                grid = self.generation()
                button = PieceButton(grid=grid)
                self.piece_button.append(button)
                self.add_widget(button)
        else:
            self.level = LEVELS.get(self.id_level)
            self.piece_button = []
            for piece in self.level["Pieces"]:
                button = PieceButton(grid=piece["Grid"])
                self.piece_button.append(button)
                self.add_widget(button)
    
    def generation(self):
        color = random.randint(1, 6)
        tier = random.randint(1, self.tiers)
        pieces = PIECES.get(tier)
        piece = pieces[random.randint(0, len(pieces)-1)]
        grid = []
        for y in range(len(piece)):
            grid.append([])
            for x  in range(len(piece[y])):
                if piece[y][x] == 0:
                    grid[y].append(color)
                else:
                    grid[y].append(None)
        for i in range(random.randint(0, 3)):
            grid = self.turn(grid)
        self.piece_generated += 1
        if self.piece_generated > 90:
            self.tiers = int(self.piece_generated//30)
        if self.tiers > 13:
            self.tiers = 13
        return grid

    def turn(self, grid):
        new_grid = []
        for y in range(len(grid[0])):
            new_grid.append([])
            for x in range(len(grid)):
                new_grid[y].append(None)
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                new_grid[-(x+1)][y] = grid[y][x]
        return new_grid

class MyScrollView(ScrollView, Loop):
    id_level = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid_piece = GridPiece(id_level=self.id_level)
        self.add_widget(self.grid_piece)
    
    def loop(self, *args):
        self.disabled = self.parent.parent.message != None


class ZonePieces(BoxLayout, Loop):
    id_level = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.my_scroll_view = MyScrollView(id_level=self.id_level)
        self.add_widget(self.my_scroll_view)
    
    def loop(self, *args):
        self.height = self.parent.height - self.parent.grid_image.height - 0.15*self.parent.height


class Grid(RelativeLayout, Loop):
    id_level = NumericProperty(None)
    victoire = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.id_level == 0:
            self.grid = generate_grid(4)
        else:
            self.level = LEVELS.get(self.id_level)
            self.grid = self.level["Grid"]
        self.nb_l = len(self.grid)
        self.nb_c = len(self.grid[0])
        self.size_hint = (None, None)
    
    def loop(self, *args):
        # Change la pos et la size du RelativeLayout
        self.width = self.parent.grid_image.width * 0.75
        self.height = self.width
        self.center_x = self.parent.grid_image.center_x
        self.center_y = self.parent.grid_image.center_y
        dispaly_grid(self=self, background=True, border=True, relative=True)
        if self.id_level != 0 and not self.victoire:
            for y in self.grid:
                for x in y:
                    if type(x) != int:
                        return
            self.victoire = True
            self.parent.message = VictoireMessage(id_level=self.id_level)
            self.parent.add_widget(self.parent.message)


class Arrow(Button, Loop):
    def loop(self, *args):
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


class Page(FloatLayout, Loop):
    score = NumericProperty(0)
    id_level = NumericProperty(None)
    mode = ListProperty(None)
    arrows = BooleanProperty(True)
    undo_consecutif = NumericProperty(0)
    saves = ListProperty([])
    undo_saves = ListProperty([])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = None
        self.current_piece = None
        self.grid_image = GridImage()
        self.grid = Grid(id_level=self.id_level)
        self.zone_piece = ZonePieces(id_level=self.id_level)
        self.undo_button = UndoButton()
        self.menu_button = MenuButton()
        if self.arrows or self.id_level == 0:
            self.add_widget(RightArrow())
            self.add_widget(LeftArrow())
        self.redo_button = None
        self.score_label = None
        if self.id_level != 0:
            self.redo_button = RedoButton()
            self.add_widget(self.redo_button)
        else:
            self.score_label = ScoreCase(text=str(self.score))
            self.add_widget(self.score_label)
        self.add_widget(self.grid_image)
        self.add_widget(self.grid)
        self.add_widget(self.zone_piece)
        self.add_widget(self.undo_button)
        self.add_widget(self.menu_button)
        if SETTINGS.get("Best_score")[0] == 0 and self.id_level == 0:
            self.message = InfoMessage(message=("Bienvenue dans le\n mode infini de Cubis !", "Dans ce mode,\nle but est de remplir le\nplus possible de grilles.", "Vous aurez à chaque fois\n6 pièces pour la remplir.","A chaque pièce posé,\nvous en regagnerez une autre.", "Le but est donc de faire\nle meilleur score possible.", "Vous avez le droit de tourner\nles pièces autant de fois\nque vous le souhaitez.", "Mais un seul retour\nen arrière possible !", "Bonne chance !"))
            self.add_widget(self.message)
        if self.id_level == SETTINGS.get("Current_level"):
            try:
                message = LEVELS.get(self.id_level)["Message"]
                self.message = InfoMessage(message=message)
                self.add_widget(self.message)
            except:
                # Il n'y a pas de messages
                pass
    
    def loop(self, *args):
        if self.id_level == 0:
            self.undo_button.disabled = (not (len(self.saves) >= 1 or self.current_piece != None)) or (self.undo_consecutif == 1)
            # Verifie si la grille est remplit
            for y in self.grid.grid:
                for x in y:
                    if type(x) != int:
                        return
            # Si oui, on regenère la grille suivant les tiers
            tiers = self.zone_piece.my_scroll_view.grid_piece.tiers
            if tiers <= 5:
                self.grid.grid = generate_grid(4)
            elif tiers <= 7:
                self.grid.grid = generate_grid(5)
            elif tiers <= 9:
                self.grid.grid = generate_grid(6)
            elif tiers <= 11:
                self.grid.grid = generate_grid(7)
            else:
                self.grid.grid = generate_grid(8)
            self.saves = []
        else:
            self.redo_button.disabled = len(self.undo_saves) < 1
            self.undo_button.disabled = not (len(self.saves) >= 1 or self.current_piece != None)
    
    def on_touch_up(self, touch):
        if self.message:
            return
        if self.verify():
            self.save()
            self.marg = int(self.grid.size_line/2)
            # Modifie la grille pour ajouter la pièce
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
            if self.id_level == 0:
                score = 0
                for y in self.current_piece.grid:
                    for x in y:
                        if x != None:
                            score += 1
                self.score += score * score
                self.score_label.text = str(self.score)
            piece_find = False
            while not piece_find:
                for piece in self.zone_piece.my_scroll_view.grid_piece.piece_button:
                    if piece.grid == self.current_piece.grid and not piece_find:
                        piece_find = True
                        self.zone_piece.my_scroll_view.grid_piece.piece_button.remove(piece)
                        self.zone_piece.my_scroll_view.grid_piece.remove_widget(piece)
                self.left()
            self.current_piece = None
            if self.id_level ==0:
                grid = self.zone_piece.my_scroll_view.grid_piece.generation()
                button = PieceButton(grid=grid)
                self.zone_piece.my_scroll_view.grid_piece.piece_button.append(button)
                self.zone_piece.my_scroll_view.grid_piece.add_widget(button)
    
    def save(self, redo=False):
        if self.id_level == 0:
            grid = copy.deepcopy(self.grid.grid)
            score = copy.deepcopy(self.score)
            pieces = []
            for piece in self.zone_piece.my_scroll_view.grid_piece.piece_button:
                pieces.append(piece.grid)
            if self.undo_consecutif == 1:
                self.undo_consecutif = 0
            else:
                self.saves.append((grid, pieces, score))
            if len(self.saves) > 1:
                self.saves.pop(0)
        else:
            if not redo:
                self.undo_saves = []
            grid = copy.deepcopy(self.grid.grid)
            pieces = []
            for piece in self.zone_piece.my_scroll_view.grid_piece.piece_button:
                pieces.append(piece.grid)
            self.saves.append((grid, pieces))
    
    def undo_save(self):
        grid = copy.deepcopy(self.grid.grid)
        pieces = []
        for piece in self.zone_piece.my_scroll_view.grid_piece.piece_button:
            pieces.append(piece.grid)
        self.undo_saves.append((grid, pieces))
    
    def undo(self):
        if self.id_level == 0:
            if self.current_piece:
                self.remove_widget(self.current_piece)
                self.current_piece = None
                return
            self.undo_consecutif = 1
            self.grid.grid = self.saves[-1][0]
            self.zone_piece.my_scroll_view.grid_piece.piece_button = []
            self.zone_piece.my_scroll_view.grid_piece.clear_widgets()
            for piece in self.saves[-1][1]:
                button = PieceButton(grid=piece)
                self.zone_piece.my_scroll_view.grid_piece.piece_button.append(button)
                self.zone_piece.my_scroll_view.grid_piece.add_widget(button)
            self.score = self.saves[-1][2]
            self.score_label.text = str(self.score)
            self.saves.pop(-1)
        else:
            if self.current_piece:
                self.remove_widget(self.current_piece)
                self.current_piece = None
                return
            self.undo_save()
            self.grid.grid = self.saves[-1][0]
            self.zone_piece.my_scroll_view.grid_piece.piece_button = []
            self.zone_piece.my_scroll_view.grid_piece.clear_widgets()
            for grid in self.saves[-1][1]:
                button = PieceButton(grid=grid)
                self.zone_piece.my_scroll_view.grid_piece.piece_button.append(button)
                self.zone_piece.my_scroll_view.grid_piece.add_widget(button)
            self.saves.pop(-1)
    
    def redo(self):
        if self.current_piece != None:
            self.remove_widget(self.current_piece)
            self.current_piece = None
            return
        self.save(redo=True)
        self.grid.grid = copy.deepcopy(self.undo_saves[-1][0])
        self.zone_piece.my_scroll_view.grid_piece.piece_button = []
        self.zone_piece.my_scroll_view.grid_piece.clear_widgets()
        for grid in self.undo_saves[-1][1]:
            button = PieceButton(grid=grid)
            self.zone_piece.my_scroll_view.grid_piece.piece_button.append(button)
            self.zone_piece.my_scroll_view.grid_piece.add_widget(button)
        self.undo_saves.pop(-1)
    
    def change_current_piece(self, grid):
        if self.current_piece != None:
            self.remove_widget(self.current_piece)
        self.current_piece = CurrentPiece(grid=grid)
        self.add_widget(self.current_piece)

    def message_push(self):
        if not self.message:
            self.message = MenuMessage(score=self.score, id_level=self.id_level)
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
                return all(check)
        except:
            return False

    def right(self):
        if self.current_piece != None:
            self.current_piece.right()

    def left(self):
        if self.current_piece != None:
            self.current_piece.left()


class Game(Screen):
    id_level = NumericProperty(None)
    
    def restart(self, id_level):
        self.clear_widgets()
        self.id_level = id_level
        self.my_float = FloatLayout()
        if id_level == 0:
            self.page = Page(id_level=self.id_level)
            self.background = "../images/backgrounds/space.jpg"
        else:
            for area in AREAS.get("all"):
                for level in area["Levels"]:
                    if level["Id"] == self.id_level:
                        self.mode = level["Mode"]
                        self.background = area["Background"]
            self.arrows = "Rotation" in self.mode
            self.page = Page(arrows=self.arrows, id_level=self.id_level, mode=self.mode)
        self.my_float.add_widget(Image(source=self.background, fit_mode="cover"))
        self.my_float.add_widget(self.page)
        self.add_widget(self.my_float)