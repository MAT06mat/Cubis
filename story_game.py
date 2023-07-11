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
from kivy.metrics import dp

from message import MenuMessage, VictoireMessage, InfoMessage
from data import SETTINGS, AREAS, LEVELS
from infinite_game import get_max_y, get_min_x, dispaly_grid, RightArrow, LeftArrow, CurrentPiece, GridImage, PieceButton, UndoButton, RedoButton

import copy

Builder.load_file("story_game.kv")


class GridPiece(GridLayout):
    def __init__(self, current_level, **kwargs):
        super().__init__(**kwargs)
        self.current_level = current_level
        self.piece_button = []
        for piece in self.current_level["Pieces"]:
            button = PieceButton(grid=piece["Grid"])
            self.piece_button.append(button)
            self.add_widget(button)


class MyScrollView(ScrollView):
    def __init__(self, current_level, **kwargs):
        super().__init__(**kwargs)
        self.current_level = current_level
        self.grid_piece = GridPiece(current_level=self.current_level)
        self.add_widget(self.grid_piece)
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        self.disabled = self.parent.parent.message != None


class ZonePieces(BoxLayout):
    def __init__(self, level, **kwargs):
        super().__init__(**kwargs)
        self.level = level
        self.my_scroll_view = MyScrollView(current_level=level)
        self.add_widget(self.my_scroll_view)
        Clock.schedule_interval(self.resize, 1/60)
    
    def resize(self, *args):
        self.height = self.parent.height - self.parent.grid_image.height - 0.15*self.parent.height


class Grid(RelativeLayout):
    def __init__(self, level, id_level, **kwargs):
        super().__init__(**kwargs)
        self.id_level = id_level
        self.grid = level["Grid"]
        self.nb_l = len(self.grid)
        self.nb_c = len(self.grid[0])
        self.pieces = level["Pieces"]
        self.size_hint = (None, None)
        self.victoire = False
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        # Change la pos et la size du RelativeLayout
        self.width = self.parent.grid_image.width * 0.75
        self.height = self.width
        self.center_x = self.parent.grid_image.center_x
        self.center_y = self.parent.grid_image.center_y
        dispaly_grid(self=self, background=True, border=True, relative=True)
        if not self.victoire:
            for y in self.grid:
                for x in y:
                    if type(x) != int:
                        return
            self.victoire = True
            self.parent.message = VictoireMessage(id_level=self.id_level)
            self.parent.add_widget(self.parent.message)


class Page(FloatLayout):
    def __init__(self, arrows, id_level, mode, **kwargs):
        super().__init__(**kwargs)
        if arrows:
            self.add_widget(RightArrow())
            self.add_widget(LeftArrow())
        self.level = LEVELS.get(id_level)
        self.id_level = id_level
        self.mode = mode
        self.current_piece = None
        self.message = None
        self.mouse_pos = None
        self.can_place = False
        self.saves = []
        self.undo_saves = []
        self.grid = Grid(level=self.level, id_level=self.id_level)
        self.zone_piece = ZonePieces(level=self.level)
        self.undo_button = UndoButton()
        self.redo_button = RedoButton()
        self.grid_image = GridImage()
        self.add_widget(self.grid_image)
        self.add_widget(self.grid)
        self.add_widget(self.zone_piece)
        self.add_widget(self.undo_button)
        self.add_widget(self.redo_button)
        Clock.schedule_interval(self.loop, 1/60)
        try:
            if self.id_level == SETTINGS.get("Current_level"):
                message = self.level["Message"]
                self.message = InfoMessage(message=message)
                self.add_widget(self.message)
        except:
            # Il n'y a pas de messages
            pass
    
    def loop(self, *args):
        self.undo_button.disabled = not (len(self.saves) >= 1 or self.current_piece != None)
        self.redo_button.disabled = len(self.undo_saves) < 1
        self.verify()    
    
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
    
    def save(self, redo=False):
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
        self.current_piece = CurrentPiece(grid)
        self.add_widget(self.current_piece)

    def right(self):
        if self.current_piece != None:
            self.current_piece.right()

    def left(self):
        if self.current_piece != None:
            self.current_piece.left()
    
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


class StoryGame(Screen):
    def __init__(self, id_level, **kw):
        super().__init__(**kw)
        self.id_level = id_level
        self.level_name = "Niveau " + str(id_level)
        for area in AREAS.get("all"):
            for level in area["Levels"]:
                if level["Id"] == id_level:
                    self.mode = level["Mode"]
                    self.background = area["Background"]
        self.arrows = "Rotation" in self.mode
        self.my_float = FloatLayout()
        self.my_float.add_widget(Image(source=self.background, fit_mode="cover"))
        self.my_float.add_widget(Page(arrows=self.arrows, id_level=id_level, mode=self.mode))
        self.add_widget(self.my_float)
        