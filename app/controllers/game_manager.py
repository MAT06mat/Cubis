from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
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
from models.data import SETTINGS, PIECES, AREAS, LEVELS, TEXTS
from models.decorators import if_no_message, if_no_piece
from controllers.message import MenuMessage, InfoMessage, VictoireMessage

import os
import copy
import random

current_directory = os.path.dirname(os.path.realpath(__file__))
kv_file_path = os.path.join(current_directory, "../views/game.kv")
Builder.load_file(kv_file_path)

COLOR = ((0.65, 0.65, 0.65), (1, 0, 0), (0, 0, 1), (0, 1, 0), (1, 1, 0), (1, 0, 1), (0, 1, 1))
ANIMATION_LIST = []

def get_min_x(self):
    return self.width/2-self.size_line_h/2
def get_max_x(self):
    return self.width/2+self.size_line_h/2
def get_min_y(self):
    return self.height/2-self.size_line_v/2
def get_max_y(self):
    return self.height/2+self.size_line_v/2

def line_size_calculation(self):
    if self.nb_l >= self.nb_c:
        self.size_line = self.height/self.nb_l
        self.size_line_v = self.height
        self.size_line_h = self.size_line*self.nb_c
    else:
        self.size_line = self.width/self.nb_c
        self.size_line_v = self.size_line*self.nb_l
        self.size_line_h = self.width

def dispaly_grid(self, background=False, border=False, relative=False, animation=False, border_block=False):
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
                Color(*color, opacity)
                Rectangle(pos=(rel_x+get_min_x(self)+x*self.size_line,rel_y+get_max_y(self)-(y+1)*self.size_line), size=(self.size_line, self.size_line), source=f"assets/images/elements/{block}.png")
        if border_block:
            Color(0.91, 0.72, 0.27, 1)
            for y in range(len(self.grid)):
                for x in range(len(self.grid[y])):
                    if self.grid_id[y][x] == None:
                        continue
                    # Side left
                    if x == 0:
                        Line(points=(get_min_x(self)+x*self.size_line+1, get_max_y(self)-y*self.size_line, get_min_x(self)+x*self.size_line+1, get_max_y(self)-(y+1)*self.size_line), width=1.5)
                    else: 
                        if self.grid_id[y][x] != self.grid_id[y][x-1]:
                            Line(points=(get_min_x(self)+x*self.size_line+1, get_max_y(self)-y*self.size_line, get_min_x(self)+x*self.size_line+1, get_max_y(self)-(y+1)*self.size_line), width=1.5)
                    # Side top
                    if y == 0:
                        Line(points=(get_min_x(self)+x*self.size_line, get_max_y(self)-y*self.size_line-1, get_min_x(self)+(x+1)*self.size_line, get_max_y(self)-y*self.size_line-1), width=1.5)
                    else: 
                        if self.grid_id[y][x] != self.grid_id[y-1][x]:
                            Line(points=(get_min_x(self)+x*self.size_line, get_max_y(self)-y*self.size_line-1, get_min_x(self)+(x+1)*self.size_line, get_max_y(self)-y*self.size_line-1), width=1.5)
                    # Side right
                    if x+1 == len(self.grid[y]):
                        Line(points=(get_min_x(self)+(x+1)*self.size_line-1, get_max_y(self)-y*self.size_line, get_min_x(self)+(x+1)*self.size_line-1, get_max_y(self)-(y+1)*self.size_line), width=1.5)
                    else: 
                        if self.grid_id[y][x] != self.grid_id[y][x+1]:
                            Line(points=(get_min_x(self)+(x+1)*self.size_line-1, get_max_y(self)-y*self.size_line, get_min_x(self)+(x+1)*self.size_line-1, get_max_y(self)-(y+1)*self.size_line), width=1.5)
                    # Side bottom
                    if y+1 == len(self.grid):
                        Line(points=(get_min_x(self)+x*self.size_line, get_max_y(self)-(y+1)*self.size_line+1, get_min_x(self)+(x+1)*self.size_line, get_max_y(self)-(y+1)*self.size_line+1), width=1.5)
                    else: 
                        if self.grid_id[y][x] != self.grid_id[y+1][x]:
                            Line(points=(get_min_x(self)+x*self.size_line, get_max_y(self)-(y+1)*self.size_line+1, get_min_x(self)+(x+1)*self.size_line, get_max_y(self)-(y+1)*self.size_line+1), width=1.5)
        if animation:
            for animation in ANIMATION_LIST:
                # Add object
                Color(1, 1, 1, animation.object_opacity)
                Rectangle(pos=animation.animation_pos, size=animation.animation_size, source=animation.object)
                # Add animation
                Color(1, 1, 1, 1)
                Rectangle(pos=animation.animation_pos, size=animation.animation_size, source=animation.current_frame)
        """
        B__ : "Box"
        N_ : "Normal"
        M_ : "Motif"
        H_ : "Hard Block"
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
        """
    if background and not relative:
        self.background_debug.size = (self.width, self.height)
        self.background_debug.pos = self.pos
    elif background and relative:
        self.background_debug.size = (self.width, self.height)

def generate_grid(self, size):
    self.nb_l, self.nb_c = size, size
    grid = []
    for y in range(size):
        grid.append([])
        for x  in range(size):
            grid[y].append("NV")
    return grid


class BlockAnimation(Loop):
    def __init__(self, time: float, type: str, animation_pos: tuple, animation_size: tuple):
        super().__init__()
        self.timer = -1
        self.asset_directory = os.path.join(current_directory, "../assets/images/elements/")
        self.frames = os.listdir(self.asset_directory+type+"/")
        self.frames.sort()
        self.time = time
        self.time_per_frames = time//len(self.frames)
        self.type = type
        self.object = self.asset_directory+type.lower()+".png"
        self.animation_pos = animation_pos
        self.animation_size = animation_size
        self.current_frame = self.asset_directory+self.type+"/"+self.frames[0]
        self.object_opacity = 1
    
    def loop(self, *args):
        self.timer += 1
        self.object_opacity = 1-self.timer*3/self.time
        if not 0 <= self.object_opacity <= 1:
            self.object_opacity = 0
        for frame_index in range(len(self.frames)):
            if frame_index * self.time_per_frames == self.timer:
                self.current_frame = self.asset_directory+self.type+"/"+self.frames[frame_index]
        if (len(self.frames) + 1) * self.time_per_frames == self.timer:
            ANIMATION_LIST.remove(self)
            self.timer = 999999
        if self.timer > 999999:
            self.timer = 999999
    

class RedoButton(Button, Loop):
    def loop(self, *args):
        self.x = self.width*0.8
        self.y = Window.height - self.height*0.9

    @if_no_message
    @if_no_piece
    def on_press(self):
        self.parent.redo()
        return super().on_press()


class UndoButton(Button, Loop):
    def loop(self, *args):
        self.y = Window.height - self.height*0.9

    @if_no_message
    @if_no_piece
    def on_press(self):
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
            self.background_r = Rectangle(source='assets/images/elements/score.png')
    
    def loop(self, *args):
        self.x = self.parent.menu_button.x - self.width
        self.y = Window.height - self.height*0.9
        self.background_r.size = (self.size[0]*1.2, self.size[1]*0.5)
        self.background_r.pos = (self.center_x-self.background_r.size[0]/2, self.center_y-self.background_r.size[1]/2)
    

class MenuButton(Button, Loop):
    def loop(self, *args):
        self.x = Window.width - self.width*0.9
        self.y = Window.height - self.height*0.9
    
    @if_no_message
    @if_no_piece
    def on_press(self):
        self.parent.message_push()
        return super().on_press()


class CurrentPiece(RelativeLayout, Loop):
    grid = ListProperty(None)
    
    def __init__(self, size_line, **kwargs):
        super().__init__(**kwargs)
        self.nb_l = len(self.grid)
        self.nb_c = len(self.grid[0])
        self.size_hint = (None, None)
        self.size_line = size_line
        self.loop(self, None)
        self.delta_pos = (self.width/2, self.height/2)
        self.pos = (Window.mouse_pos[0] - self.delta_pos[0], Window.mouse_pos[1] - self.delta_pos[1])
        Window.bind(on_resize=self.on_window_resize)
    
    def loop(self, *args):
        try:
            self.size_line = self.parent.grid.size_line
        except:
            pass
        self.width = self.nb_c*self.size_line
        self.height = self.nb_l*self.size_line
        dispaly_grid(self, relative=True)
    
    def on_window_resize(self, *args):
        self.pos = (Window.width/2-self.width/2, Window.height/2-self.width/2)
    
    def on_touch_down(self, touch):
        if self.parent.message != None:
            return
        touch_piece = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if (self.pos[0]+self.size_line*x) < touch.pos[0] < (self.pos[0]+self.size_line*(x+1)) and (self.pos[1]+self.height-self.size_line*(y+1)) < touch.pos[1] < (self.pos[1]+self.height-self.size_line*y) and self.grid[y][x] != "NV":
                    touch_piece.append(True)
                else:
                    touch_piece.append(False)
        if any(touch_piece):
            self.delta_pos = (touch.pos[0] - self.pos[0], touch.pos[1] - self.pos[1])
        else:
            self.delta_pos = None
    
    def on_touch_move(self, touch):
        if self.parent.message != None:
            return
        if self.delta_pos != None:
            self.pos = (touch.pos[0] - self.delta_pos[0], touch.pos[1] - self.delta_pos[1])
    
    def on_touch_up(self, touch):
        if self.parent.zone_piece.x+self.parent.zone_piece.width > self.x+self.width/2 > self.parent.zone_piece.x and self.parent.zone_piece.y+self.parent.zone_piece.height > self.y+self.height/2 > self.parent.zone_piece.y:
            button = PieceButton(grid=self.grid)
            self.parent.zone_piece.my_scroll_view.grid_piece.piece_button.append(button)
            self.parent.zone_piece.my_scroll_view.grid_piece.add_widget(button)
            self.parent.current_piece = None
            self.parent.remove_widget(self)
        return super().on_touch_up(touch)
    
    def right(self):
        new_grid = [["NV" for x in self.nb_l] for y in self.nb_c]
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                new_grid[x][-(y+1)] = self.grid[y][x]
        self.grid = new_grid
        self.nb_l = len(self.grid)
        self.nb_c = len(self.grid[0])
    
    def left(self):
        new_grid = [["NV" for x in self.nb_l] for y in self.nb_c]
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                new_grid[-(x+1)][y] = self.grid[y][x]
        self.grid = new_grid
        self.nb_l = len(self.grid)
        self.nb_c = len(self.grid[0])


class PieceButton(Button, Loop):
    grid = ListProperty(None)
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.nb_l = len(self.grid)
        self.nb_c = len(self.grid[0])
        self.size_hint = (None, None)
    
    def on_press(self):
        if self.parent.parent.parent.parent.current_piece != None:
            if self.parent.parent.parent.parent.current_piece.delta_pos == None:
                pass
            else:
                return super().on_press()
        if self.parent.parent.parent.parent.message != None:
            return super().on_press()
        self.parent.parent.parent.parent.change_current_piece(grid=self.grid)
        self.parent.piece_button.remove(self)
        self.parent.remove_widget(self)
        return super().on_press()
    
    def loop(self, *args):
        if self.parent != None:
            self.size_line = self.parent.parent.parent.parent.grid.size_line
            self.width = self.size_line * self.nb_c
            self.height = self.size_line * self.nb_l
        dispaly_grid(self)


class GridPiece(StackLayout):
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
            self.level = LEVELS.get()[str(self.id_level)]
            self.piece_button = []
            for piece in self.level["Pieces"]:
                button = PieceButton(grid=piece["Grid"])
                self.piece_button.append(button)
                self.add_widget(button)
    
    def generation(self):
        color = random.randint(1, 6)
        tier = random.randint(1, self.tiers)
        pieces = PIECES.get()[str(tier)]
        grid = pieces[random.randint(0, len(pieces)-1)]
        for y in range(len(grid)):
            for x  in range(len(grid[y])):
                if grid[y][x] == "GC":
                    grid[y][x] = "N" + str(color)
        for i in range(random.randint(0, 3)):
            grid = self.turn(grid)
        self.piece_generated += 1
        if self.piece_generated > 90:
            self.tiers = int(self.piece_generated//30)
        if self.tiers > 13:
            self.tiers = 13
        return grid

    def turn(self, grid):
        new_grid = [["NV" for x in grid] for y in grid[0]]
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                new_grid[-(x+1)][y] = grid[y][x]
        return new_grid

class MyScrollView(ScrollView, Loop):
    id_level = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll_type = ["bars"]
        self.bar_width = dp(8) #A04623
        self.bar_color = "#E28840"
        self.bar_inactive_color = "#E28840"
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
            self.grid = generate_grid(self, 4)
        else:
            self.level = LEVELS.get()[str(self.id_level)]
            self.grid = self.level["Grid"]
        self.nb_l = len(self.grid)
        self.nb_c = len(self.grid[0])
        self.grid_id = [[None for x in self.grid[0]] for y in self.grid]
        self.size_hint = (None, None)
    
    def test_grid(self):
        for y in self.grid:
            for x in y:
                if (x[0] != "N" and x[0] != "H") or x == "NV":
                    return True
        return False
    
    def replace_box(self):
        for y in self.grid:
            for x in y:
                if x[0] == "M" or x == "NV":
                    return
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x][0] == "B":
                    self.grid[y][x] = self.grid[y][x][1] + self.grid[y][x][2]
                    line_size_calculation(self)
                    pos=(get_min_x(self)+x*self.size_line,get_max_y(self)-(y+1)*self.size_line)
                    size=(self.size_line, self.size_line)
                    animation = BlockAnimation(time=18, type="Box", animation_pos=pos, animation_size=size)
                    ANIMATION_LIST.append(animation)
    
    def loop(self, *args):
        # Change la pos et la size du RelativeLayout
        self.width = self.parent.grid_image.width * 0.75
        self.height = self.width
        self.center_x = self.parent.grid_image.center_x
        self.center_y = self.parent.grid_image.center_y
        dispaly_grid(self=self, background=True, border=True, relative=True, animation=True, border_block=True)
        self.replace_box()
        # Verifie si la grille est remplit
        if self.test_grid():
            return
        if self.id_level != 0 and not self.victoire:
            self.victoire = True
            self.parent.message = VictoireMessage(id_level=self.id_level)
            self.parent.add_widget(self.parent.message)
        elif self.id_level == 0:
            # Si oui, on regenère la grille suivant les tiers
            tiers = self.parent.zone_piece.my_scroll_view.grid_piece.tiers
            if 0 < tiers <= 5:
                self.grid = generate_grid(self, 4)
            elif 5 < tiers <= 7:
                self.grid = generate_grid(self, 5)
            elif 7 < tiers <= 9:
                self.grid = generate_grid(self, 6)
            elif 9 < tiers <= 11:
                self.grid = generate_grid(self, 7)
            else:
                self.grid = generate_grid(self, 8)
            self.parent.saves = []
        self.grid_id = [[None for x in self.grid[0]] for y in self.grid]


class Arrow(Button, Loop):
    def loop(self, *args):
        self.width = self.height
        self.y = self.parent.grid_image.y - self.height/1.2


class RightArrow(Arrow):
    @if_no_message
    @if_no_piece
    def on_press(self):
        self.parent.current_piece.right()
        return super().on_press()


class LeftArrow(Arrow):
    @if_no_message
    @if_no_piece
    def on_press(self):
        self.parent.current_piece.left()
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
        self.new_id = 0
        self.grid_image = GridImage()
        self.grid = Grid(id_level=self.id_level)
        self.zone_piece = ZonePieces(id_level=self.id_level)
        self.undo_button = UndoButton()
        self.menu_button = MenuButton()
        if self.arrows:
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
        if SETTINGS.get()["Best_score"][0] == 0 and self.id_level == 0:
            self.message = InfoMessage(message=TEXTS.key(0))
            self.add_widget(self.message)
        elif self.id_level == SETTINGS.get()["Current_level"] and "Message" in LEVELS.get()[str(self.id_level)]:
            message_key = LEVELS.get()[str(self.id_level)]["Message"]
            message = TEXTS.key(message_key)
            self.message = InfoMessage(message=message)
            self.add_widget(self.message)
    
    def loop(self, *args):
        if self.id_level == 0:
            self.undo_button.disabled = (not (len(self.saves) >= 1 or self.current_piece != None)) or (self.undo_consecutif == 1)
        else:
            self.redo_button.disabled = len(self.undo_saves) < 1
            self.undo_button.disabled = not (len(self.saves) >= 1 or self.current_piece != None)
    
    def on_touch_up(self, touch):
        if self.message:
            return super().on_touch_up(touch)
        if self.verify():
            self.save()
            self.marg = int(self.grid.size_line/2)
            self.new_id += 1
            # Modifie la grille pour ajouter la pièce
            for y_p in range(len(self.current_piece.grid)):
                for x_p in range(len(self.current_piece.grid[y_p])):
                    if self.current_piece.grid[y_p][x_p] != "NV":
                        for y_g in range(len(self.grid.grid)):
                            for x_g in range(len(self.grid.grid[y_g])):
                                # Calculation Global of x and y for piece and grid
                                x_piece = get_min_x(self.current_piece)+self.current_piece.x+x_p*self.current_piece.size_line
                                y_piece = get_max_y(self.current_piece)+self.current_piece.y-(y_p+1)*self.current_piece.size_line
                                x_grid = get_min_x(self.grid)+self.grid.x+x_g*self.grid.size_line
                                y_grid = get_max_y(self.grid)+self.grid.y-(y_g+1)*self.grid.size_line
                                # if grid block match with piece block and if is void or if is a motifs
                                if abs(x_piece - x_grid) < self.marg and abs(y_piece - y_grid) < self.marg and (self.grid.grid[y_g][x_g] == "NV" or (self.grid.grid[y_g][x_g][0] == "M" and self.current_piece.grid[y_p][x_p][1] == self.grid.grid[y_g][x_g][1])):
                                    self.grid.grid[y_g][x_g] = self.current_piece.grid[y_p][x_p]
                                    self.grid.grid_id[y_g][x_g] = self.new_id
            self.remove_widget(self.current_piece)
            if self.id_level == 0:
                score = 0
                for y in self.current_piece.grid:
                    for x in y:
                        if x != "NV":
                            score += 1
                self.score += score * score
                self.score_label.text = str(self.score)
            self.current_piece = None
            if self.id_level ==0:
                grid = self.zone_piece.my_scroll_view.grid_piece.generation()
                button = PieceButton(grid=grid)
                self.zone_piece.my_scroll_view.grid_piece.piece_button.append(button)
                self.zone_piece.my_scroll_view.grid_piece.add_widget(button)
        return super().on_touch_up(touch)
    
    def save(self, redo=False):
        if self.id_level == 0:
            grid = copy.deepcopy(self.grid.grid)
            score = copy.deepcopy(self.score)
            grid_id = copy.deepcopy(self.grid.grid_id)
            pieces = []
            for piece in self.zone_piece.my_scroll_view.grid_piece.piece_button:
                pieces.append(piece.grid)
            if self.current_piece != None:
                pieces.append(self.current_piece.grid)
            if self.undo_consecutif == 1:
                self.undo_consecutif = 0
            else:
                self.saves.append({"grid":grid, "pieces":pieces, "score":score, "grid_id":grid_id})
            if len(self.saves) > 1:
                self.saves.pop(0)
        else:
            if not redo:
                self.undo_saves = []
            grid = copy.deepcopy(self.grid.grid)
            grid_id = copy.deepcopy(self.grid.grid_id)
            pieces = []
            for piece in self.zone_piece.my_scroll_view.grid_piece.piece_button:
                pieces.append(piece.grid)
            if self.current_piece != None:
                pieces.append(self.current_piece.grid)
            self.saves.append({"grid":grid, "pieces":pieces, "grid_id":grid_id})
    
    def undo_save(self):
        grid = copy.deepcopy(self.grid.grid)
        grid_id = copy.deepcopy(self.grid.grid_id)
        pieces = []
        for piece in self.zone_piece.my_scroll_view.grid_piece.piece_button:
            pieces.append(piece.grid)
        if self.current_piece != None:
            pieces.append(self.current_piece.grid)
        self.undo_saves.append({"grid":grid, "pieces":pieces, "grid_id":grid_id})
    
    def undo(self):
        if self.id_level == 0:
            if self.current_piece:
                self.remove_current_piece()
                return
            self.undo_consecutif = 1
            self.grid.grid = self.saves[-1]["grid"]
            self.grid.grid_id = self.saves[-1]["grid_id"]
            self.zone_piece.my_scroll_view.grid_piece.piece_button = []
            self.zone_piece.my_scroll_view.grid_piece.clear_widgets()
            for piece in self.saves[-1]["pieces"]:
                button = PieceButton(grid=piece)
                self.zone_piece.my_scroll_view.grid_piece.piece_button.append(button)
                self.zone_piece.my_scroll_view.grid_piece.add_widget(button)
            self.score = self.saves[-1]["score"]
            self.score_label.text = str(self.score)
            self.saves.pop(-1)
        else:
            if self.current_piece != None:
                self.remove_current_piece()
                return
            self.undo_save()
            self.grid.grid = self.saves[-1]["grid"]
            self.grid.grid_id = self.saves[-1]["grid_id"]
            self.zone_piece.my_scroll_view.grid_piece.piece_button = []
            self.zone_piece.my_scroll_view.grid_piece.clear_widgets()
            for grid in self.saves[-1]["pieces"]:
                button = PieceButton(grid=grid)
                self.zone_piece.my_scroll_view.grid_piece.piece_button.append(button)
                self.zone_piece.my_scroll_view.grid_piece.add_widget(button)
            self.saves.pop(-1)
    
    def redo(self):
        if self.current_piece != None:
            self.remove_current_piece()
            return
        self.save(redo=True)
        self.grid.grid = copy.deepcopy(self.undo_saves[-1]["grid"])
        self.grid.grid_id = copy.deepcopy(self.undo_saves[-1]["grid_id"])
        self.zone_piece.my_scroll_view.grid_piece.piece_button = []
        self.zone_piece.my_scroll_view.grid_piece.clear_widgets()
        for grid in self.undo_saves[-1]["pieces"]:
            button = PieceButton(grid=grid)
            self.zone_piece.my_scroll_view.grid_piece.piece_button.append(button)
            self.zone_piece.my_scroll_view.grid_piece.add_widget(button)
        self.undo_saves.pop(-1)
    
    def change_current_piece(self, grid):
        self.remove_current_piece()
        self.current_piece = CurrentPiece(grid=grid, size_line=self.grid.size_line)
        self.add_widget(self.current_piece)

    def remove_current_piece(self):
        if self.current_piece != None:
            self.remove_widget(self.current_piece)
            button = PieceButton(grid=self.current_piece.grid)
            self.zone_piece.my_scroll_view.grid_piece.piece_button.append(button)
            self.zone_piece.my_scroll_view.grid_piece.add_widget(button)
            self.current_piece = None
    
    def message_push(self):
        if not self.message:
            self.message = MenuMessage(score=self.score, id_level=self.id_level, mode=self.mode)
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
                                one.append(abs(x_piece - x_grid) < self.marg and abs(y_piece - y_grid) < self.marg and (self.grid.grid[y_g][x_g] == "NV" or (self.grid.grid[y_g][x_g][0] == "M" and self.current_piece.grid[y_p][x_p][1] == self.grid.grid[y_g][x_g][1]) or self.current_piece.grid[y_p][x_p] == "NV"))
                        check.append(any(one))
                return all(check)
        except:
            return False


class Game(Screen):
    id_level = NumericProperty(None)
    
    def restart(self, id_level):
        self.clear_widgets()
        self.id_level = id_level
        self.my_float = FloatLayout()
        if id_level == 0:
            self.mode = []
            self.arrows = True
            self.background = "assets/images/backgrounds/space.jpg"
        else:
            for area in AREAS.get():
                for level in area["Levels"]:
                    if level["Id"] == self.id_level:
                        self.mode = level["Mode"]
                        self.background = area["Background"]
            self.arrows = 25 in self.mode
        self.page = Page(arrows=self.arrows, id_level=self.id_level, mode=self.mode)
        self.my_float.add_widget(Image(source=self.background, fit_mode="cover"))
        self.my_float.add_widget(self.page)
        self.add_widget(self.my_float)