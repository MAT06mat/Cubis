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
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, BooleanProperty, ObjectProperty
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import PushMatrix, PopMatrix, Rotate
from kivy.animation import Animation
from kivy.metrics import dp

from data import *
from models import *
from uix import *

from math import sqrt
import os
import copy


Builder.load_file("screens/game_screen.kv")


class BlockAnimation(Widget, Loop):
    frame = NumericProperty(0)
    object_opacity = NumericProperty(100)
    
    def __init__(self, time: float, type: str, animation_pos: tuple, animation_size: tuple):
        super().__init__()
        current_directory = os.path.dirname(os.path.realpath(__file__))
        self.asset_directory = os.path.join(current_directory, "../assets/images/elements/")
        self.frames = os.listdir(self.asset_directory+type+"/"+type.lower()+"/")
        self.frames.sort()
        self.anim = Animation(duration=time, frame=len(self.frames))
        self.anim &= Animation(duration=time*0.7, object_opacity=0)
        self.anim.start(self)
        self.type = type
        self.object = self.asset_directory+type+"/"+"0.png"
        self.animation_pos = animation_pos
        self.animation_size = animation_size
        self.current_frame = self.asset_directory+type+"/"+type.lower()+"/"+self.frames[0]
    
    def loop(self, *args):
        if self.frame < len(self.frames):
            self.current_frame = self.asset_directory+self.type+"/"+self.type.lower()+"/"+self.frames[int(self.frame)]
        else:
            ANIMATION_LIST.remove(self)
            return False


class HoleAnimation(Widget):
    def __init__(self, color: str, animation_pos: tuple):
        super().__init__()
        self.type = "Hole"
        self.color = color
        self.animation_pos = animation_pos
        self.opacity = 1
        self.animation = Animation(duration=0.4, opacity=0)
        self.animation.start(self)


class RedoButton(CustomResizeButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.disabled = True
    
    def loop(self, *args):
        self.x = self.width*1.2
        self.y = Window.height - self.height*1.1
        if Window.width*0.75 < Window.height:
            self.size_hint = (None, 0.06)
            self.width = self.height
        else:
            self.size_hint = (0.06, None)
            self.height = self.width
        return super().loop(*args)
    
    def condition(self):
        if self.parent.message:
            return False
        if self.parent.current_piece:
            if self.parent.current_piece.delta_pos:
                return False
        return True
    
    def on_custom_press(self, *args):
        self.parent.redo()
        return super().on_custom_press(*args)


class UndoButton(CustomResizeButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.disabled = True
    
    def loop(self, *args):
        self.x = self.width*0.1
        self.y = Window.height - self.height*1.1
        if Window.width*0.75 < Window.height:
            self.size_hint = (None, 0.06)
            self.width = self.height
        else:
            self.size_hint = (0.06, None)
            self.height = self.width
        return super().loop(*args)
    
    def condition(self):
        if self.parent.message:
            return False
        if self.parent.current_piece:
            if self.parent.current_piece.delta_pos:
                return False
        return True
    
    def on_custom_press(self, *args):
        self.parent.undo()
        return super().on_custom_press(*args)


class GridImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_resize=self.on_window_resize)
        self.on_window_resize()

    def on_window_resize(self, *args):
        if Window.width*0.75 < Window.height:
            self.pos_hint = {"center_x": 0.5, "top": 0.94}
            self.width = Window.width
            self.height = self.width
            if self.height > 0.6 * Window.height:
                self.height = 0.6 * Window.height
            if self.width > self.height:
                self.width = self.height
        else:
            self.pos_hint = {"x": 0.05, "center_y": 0.5}
            self.height = Window.height
            self.width = self.height
            if self.height > 0.8 * Window.height:
                self.height = 0.8 * Window.height
            if self.width > self.height:
                self.width = self.height


class ScoreCase(Label, Loop):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, 0.07)
        self.pos_hint = {"top": 1}
        self.width = self.height
        with self.canvas.before:
            self.background_r = Rectangle(source='assets/images/elements/score.png')
    
    def loop(self, *args):
        self.x = Window.width - (self.parent.menu_button.width*1.5 + self.width)
        self.font_size = self.height/4
        self.background_r.size = (Window.height*0.12, Window.height*0.05)
        self.background_r.pos = (self.center_x-self.background_r.size[0]/2, self.center_y-self.background_r.size[1]/2)
        return super().loop(*args)


class MenuButton(CustomResizeButton):
    def loop(self, *args):
        self.x = Window.width - self.width*1.1
        self.y = Window.height - self.height*1.1
        if Window.width*0.75 < Window.height:
            self.size_hint = (None, 0.06)
            self.width = self.height
        else:
            self.size_hint = (0.06, None)
            self.height = self.width
        return super().loop(*args)
    
    def condition(self):
        if self.parent.message:
            return False
        if self.parent.current_piece:
            if self.parent.current_piece.delta_pos:
                return False
        return True
    
    def on_custom_press(self, *args):
        self.parent.message_push()
        return super().on_custom_press(*args)


class CurrentPiece(RelativeLayout, Loop, DisplayGrid):
    grid = ListProperty(None)
    
    def __init__(self, size_line, pos, delta_pos, **kwargs):
        super().__init__(**kwargs)
        self.angle = 0
        self.anim = Animation(angle=0, duration=0.2, t="in_out_quad")
        with self.canvas.before:
            PushMatrix()
            self.rotation = Rotate(angle=self.angle, origin=self.center, axis=(0, 0, 1))
        with self.canvas.after:
            PopMatrix()
        self.size_hint = (None, None)
        self.size_line = size_line
        self.loop(None)
        self.pos = pos
        self.delta_pos = delta_pos
        Window.bind(on_resize=self.on_window_resize)
    
    def loop(self, *args):
        try:
            self.size_line = self.parent.grid.size_line
        except:
            pass
        if round(self.width, 2) != round(len(self.grid[0])*self.size_line, 2) or round(self.height, 2) != round(len(self.grid)*self.size_line, 2):
            center_x = copy.deepcopy(self.center_x)
            center_y = copy.deepcopy(self.center_y)
            self.width = len(self.grid[0])*self.size_line
            self.height = len(self.grid)*self.size_line
            self.center_x = center_x
            self.center_y = center_y
        self.rotation.origin = (self.width/2, self.height/2)
        self.rotation.angle = self.angle
        self.display_grid(relative=True, reload=self.reload, angle=self.angle)
        return super().loop(*args)
    
    def on_window_resize(self, *args):
        self.pos = (Window.width/2-self.width/2, Window.height/2-self.width/2)
    
    def on_touch_down(self, touch):
        if self.parent.message:
            return super().on_touch_down(touch)
        if self.touch_piece(touch):
            self.delta_pos = (touch.pos[0] - self.pos[0], touch.pos[1] - self.pos[1])
        else:
            self.delta_pos = None
        return super().on_touch_down(touch)
    
    def touch_piece(self, touch):
        touch_piece = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if (self.pos[0]+self.size_line*x) < touch.pos[0] < (self.pos[0]+self.size_line*(x+1)) and (self.pos[1]+self.height-self.size_line*(y+1)) < touch.pos[1] < (self.pos[1]+self.height-self.size_line*y) and self.grid[y][x] != "NV":
                    touch_piece.append(True)
                else:
                    touch_piece.append(False)
        return any(touch_piece)
    
    def on_touch_move(self, touch):
        if self.parent.message:
            return super().on_touch_move(touch)
        if self.delta_pos:
            self.pos = (touch.pos[0] - self.delta_pos[0], touch.pos[1] - self.delta_pos[1])
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        # Format vertical ou horizontal
        if Window.width*0.75 < Window.height:
            condition = self.parent.zone_piece.y+self.parent.zone_piece.height > self.y+self.height/2
        else:
            condition = self.parent.zone_piece.x < self.x+self.width/2
        # Transform piece in button if is in the zone_piece
        if condition:
            button = PieceButton(grid=self.grid)
            pieces_list = self.parent.zone_piece.my_scroll_view.grid_piece.piece_button
            if len(pieces_list) == 0:
                self.parent.zone_piece.my_scroll_view.grid_piece.piece_button.append(button)
                index = 0
            else:
                # Find the y of the piece in the raw
                y = None
                for p in pieces_list:
                    p_pos = p.to_window(p.x, p.y)
                    if p_pos[1]+p.height+dp(5) > self.y+self.height/2:
                        y = round(p_pos[1] + p.height, 0)
                # Anti crash if y == None
                if y == None:
                    y = round(p_pos[1] + p.height, 0)
                # Take pieces in the raw
                pieces_in_raw = []
                for p in pieces_list:
                    p_pos = p.to_window(p.x, p.y)
                    if round(p_pos[1]+p.height, 0) == y:
                        pieces_in_raw.append(p)
                # Find the piece before the current piece in the col
                last_piece = None
                for p in pieces_in_raw[::-1]:
                    p_pos = p.to_window(p.x, p.y)
                    if p_pos[0]+p.width/2 > self.x+self.width/2:
                        last_piece = p
                # Calculate the index of current piece
                if last_piece:
                    index = pieces_list.index(last_piece) + 1
                else:
                    index = pieces_list.index(pieces_in_raw[0]) + len(pieces_in_raw) + 1
                self.parent.zone_piece.my_scroll_view.grid_piece.piece_button.insert(index - 1, button)
            self.parent.zone_piece.my_scroll_view.grid_piece.add_widget(button, index=len(pieces_list)-index)
            self.parent.current_piece = None
            self.parent.remove_widget(self)
        return super().on_touch_up(touch)
    
    def right(self):
        self.angle += 90
        self.anim.cancel(self)
        self.anim.start(self)
        self.grid = turn(self.grid)
    
    def left(self):
        self.angle -= 90
        self.anim.cancel(self)
        self.anim.start(self)
        self.grid = turn(self.grid, right=False)


class PieceButton(Button, Loop, DisplayGrid):
    grid = ListProperty(None)
    
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.background_color = (0, 0, 0, 0)
        self.display_grid()

    def on_touch_down(self, touch):
        if self.parent.parent.parent.parent.message:
            return super().on_touch_down(touch)
        if self.parent.parent.parent.parent.current_piece:
            if self.parent.parent.parent.parent.current_piece.delta_pos:
                return super().on_touch_down(touch)
        if not self.touch_piece(touch):
            return super().on_touch_down(touch)
        pos = self.to_window(*self.pos)
        touch_pos = self.to_window(*touch.pos)
        delta_pos = (touch_pos[0] - pos[0], touch_pos[1] - pos[1])
        self.parent.parent.parent.parent.change_current_piece(grid=self.grid, pos=pos, delta_pos=delta_pos)
        self.parent.piece_button.remove(self)
        self.reload = False
        self.parent.remove_widget(self)
        return super().on_touch_down(touch)
    
    def loop(self, *args):
        if self.parent:
            self.size_line = self.parent.parent.parent.parent.grid.size_line
            self.width = self.size_line * len(self.grid[0])
            self.height = self.size_line * len(self.grid)
        self.display_grid(reload=self.reload)
        return super().loop(*args)

    def touch_piece(self, touch):
        touch_piece = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if (self.pos[0]+self.size_line*x) < touch.pos[0] < (self.pos[0]+self.size_line*(x+1)) and (self.pos[1]+self.height-self.size_line*(y+1)) < touch.pos[1] < (self.pos[1]+self.height-self.size_line*y) and self.grid[y][x] != "NV":
                    touch_piece.append(True)
                else:
                    touch_piece.append(False)
        return any(touch_piece)


class GridPiece(StackLayout):
    piece_button = ListProperty([])
    tiers = NumericProperty(3)
    piece_generated = NumericProperty(70)
    id_level = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.id_level == 0:
            for i in range(6):
                grid = Pieces.random_piece()
                button = PieceButton(grid=grid)
                self.piece_button.append(button)
                self.add_widget(button)
        else:
            self.level = Levels[str(self.id_level)]
            self.piece_button = []
            for piece in self.level["Pieces"]:
                button = PieceButton(grid=piece["Grid"])
                self.piece_button.append(button)
                self.add_widget(button)


class MyScrollView(ScrollView, Loop):
    id_level = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll_type = ["bars"]
        self.bar_width = dp(15) #A04623 => "#E28840" => (0.89, 0.54, 0.25)
        self.bar_color = (0.89, 0.54, 0.25, 1)
        self.bar_inactive_color = (0.89, 0.54, 0.25, 0.5)
        self.grid_piece = GridPiece(id_level=self.id_level)
        self.add_widget(self.grid_piece)
    
    def loop(self, *args):
        self.disabled = self.parent.parent.message != None
        self.bar_width = round(self.width / 15, 2)
        return super().loop(*args)


class ZonePieces(BoxLayout, Loop):
    id_level = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {"right": 1}
        self.my_scroll_view = MyScrollView(id_level=self.id_level)
        self.add_widget(self.my_scroll_view)
        Window.bind(on_resize=self.on_window_resize)
        self.on_window_resize()
    
    def on_window_resize(self, *args):
        if Window.width*0.75 < Window.height:
            self.size_hint = (1, None)
            height = Window.width
            if height > 0.6 * Window.height:
                height = 0.6 * Window.height
            self.height = Window.height * 0.85 - height
        else:
            self.size_hint = (None, 0.9)
            width = Window.height
            if width > 0.8 * Window.height:
                width = 0.8 * Window.height
            self.width = Window.width * 0.92 - width


class Grid(RelativeLayout, Loop, DisplayGrid):
    id_level = NumericProperty(None)
    victoire = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.id_level == 0:
            self.grid = generate_grid(size=4)
        else:
            self.level = copy.deepcopy(Levels[str(self.id_level)])
            self.grid = self.level["Grid"]
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
                    self.line_size_calculation()
                    pos=(self.min_x+x*self.size_line,self.max_y-(y+1)*self.size_line)
                    size=(self.size_line, self.size_line)
                    animation = BlockAnimation(time=0.5, type="box", animation_pos=pos, animation_size=size)
                    ANIMATION_LIST.append(animation)
    
    def loop(self, *args):
        # Change la pos et la size du RelativeLayout
        self.width = self.parent.grid_image.width * 0.75
        self.height = self.width
        self.center_x = self.parent.grid_image.center_x
        self.center_y = self.parent.grid_image.center_y
        self.display_grid(background=True, border=True, relative=True, animation=True, border_block=True, reload=self.reload)
        self.replace_box()
        # Verifie si la grille est remplit if not : return
        if self.test_grid():
            return super().loop(*args)
        if self.id_level != 0 and not self.victoire:
            self.victoire = True
            self.parent.message = VictoireMessage(id_level=self.id_level, temp_parent=self.parent)
            self.parent.add_widget(self.parent.message)
        elif self.id_level == 0:
            # Si oui, on regenère la grille suivant ne nombre de pièces posées
            nb = Pieces.increase_int
            if nb <= 30:
                self.grid = generate_grid(size=4)
            elif nb <= 100:
                self.grid = random_grid(size=5, nb=nb)
            elif nb <= 250:
                self.grid = random_grid(size=6, nb=nb)
            elif nb <= 500:
                self.grid = random_grid(size=7, nb=nb)
            else:
                self.grid = random_grid(size=8, nb=nb)
            self.parent.saves = []
            self.grid_id = [[None for x in self.grid[0]] for y in self.grid]
        return super().loop(*args)


class Arrow(CustomResizeButton, Loop):
    arrow_type = None
    
    def loop(self, *args):
        self.y = self.parent.grid_image.y - self.height*0.9
        if Window.width*0.75 < Window.height:
            self.width = self.height
            self.size_hint = (None, 0.08)
            if self.arrow_type == "left":
                self.pos_hint = {}
                self.x = 0
            else:
                self.pos_hint = {"right": 1}
        else:
            self.size_hint = (0.05, None)
            self.height = self.width
            self.pos_hint = {}
            if self.arrow_type == "left":
                self.x = self.parent.grid_image.x
            else:
                self.x = self.parent.grid_image.x + self.parent.grid_image.width - self.width
        return super().loop(*args)

    def condition(self):
        if self.parent.message:
            return False
        if self.parent.current_piece:
            if self.parent.current_piece.delta_pos:
                return False
        return True


class RightArrow(Arrow):
    arrow_type = "right"
    
    def on_custom_press(self, *args):
        if self.parent.current_piece:
            self.parent.current_piece.right()
            Clock.schedule_once(self.parent.put_current_piece_in_grid)
        return super().on_custom_press(*args)


class LeftArrow(Arrow):
    arrow_type = "left"
    
    def on_custom_press(self, *args):
        if self.parent.current_piece:
            self.parent.current_piece.left()
            Clock.schedule_once(self.parent.put_current_piece_in_grid)
        return super().on_custom_press(*args)


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
        self.right_arrow = None
        self.left_arrow = None
        if self.arrows:
            self.right_arrow = RightArrow()
            self.left_arrow = LeftArrow()
            self.add_widget(self.right_arrow)
            self.add_widget(self.left_arrow)
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
        if self.id_level == 0:
            if Settings.best_score[0] == 0:
                self.message = InfoMessage(message=Texts.key(0), temp_parent=self)
                self.add_widget(self.message)
        else:
            if "Message" in Levels[str(self.id_level)]:
                message_key = Levels[str(self.id_level)]["Message"]
                message = Texts.key(message_key)
                self.message = InfoMessage(message=message, temp_parent=self)
                self.add_widget(self.message)
    
    def loop(self, *args):
        if self.id_level == 0:
            self.undo_button.disabled = (not (len(self.saves) >= 1 or self.current_piece != None)) or (self.undo_consecutif == 1)
        else:
            self.redo_button.disabled = len(self.undo_saves) < 1
            self.undo_button.disabled = not (len(self.saves) >= 1 or self.current_piece != None)
        return super().loop(*args)
    
    # Alow remove a piece from the grid
    """def on_touch_down(self, touch):
        if self.current_piece != None:
            if self.current_piece.touch_piece(touch):
                return super().on_touch_down(touch)
        if self.grid.x+self.grid.width > touch.pos[0] > self.grid.x and self.grid.y+self.grid.height > touch.pos[1] > self.grid.y and self.id_level != 0 and self.message == None:
            size_line = self.grid.size_line
            piece_id = None
            piece_grid = generate_grid(width=len(self.grid.grid[0]), height=len(self.grid.grid))
            for y_g in range(len(self.grid.grid)):
                for x_g in range(len(self.grid.grid[y_g])):
                    # Calculation Global of x and y for the grid
                    x_grid = self.grid.min_x+self.grid.x+x_g*self.grid.size_line
                    y_grid = self.grid.max_y+self.grid.y-(y_g+1)*self.grid.size_line
                    if x_grid+size_line > touch.pos[0] > x_grid and y_grid+size_line > touch.pos[1] > y_grid:
                        piece_id = self.grid.grid_id[y_g][x_g]
            if piece_id == None:
                return super().on_touch_down(touch)
            self.save()
            for y_g in range(len(self.grid.grid)):
                for x_g in range(len(self.grid.grid[y_g])):
                    if self.grid.grid_id[y_g][x_g] == piece_id:
                        piece_grid[y_g][x_g] = self.grid.grid[y_g][x_g]
                        self.grid.grid_id[y_g][x_g] = None
                        self.grid.grid[y_g][x_g] = "NV"
            for i in range(4):
                operation = True
                while operation:
                    operation = False
                    void = [x == "NV" for x in piece_grid[0]]
                    if all(void):
                        piece_grid.pop(0)
                        operation = True
                piece_grid = turn(piece_grid)
            self.change_current_piece(piece_grid)
        return super().on_touch_down(touch)"""
    
    def on_touch_up(self, touch):
        if self.message:
            return super().on_touch_up(touch)
        self.put_current_piece_in_grid()
        return super().on_touch_up(touch)
    
    def put_current_piece_in_grid(self, *args):
        if not self.verify():
            return
        # Add current piece to grid
        self.save()
        marg = int(self.grid.size_line/2)
        self.new_id += 1
        for y_p in range(len(self.current_piece.grid)):
            for x_p in range(len(self.current_piece.grid[y_p])):
                if self.current_piece.grid[y_p][x_p] != "NV":
                    for y_g in range(len(self.grid.grid)):
                        for x_g in range(len(self.grid.grid[y_g])):
                            # Calculation Global of x and y for piece and grid
                            x_piece = self.current_piece.min_x+self.current_piece.x+x_p*self.current_piece.size_line
                            y_piece = self.current_piece.max_y+self.current_piece.y-(y_p+1)*self.current_piece.size_line
                            x_grid = self.grid.min_x+self.grid.x+x_g*self.grid.size_line
                            y_grid = self.grid.max_y+self.grid.y-(y_g+1)*self.grid.size_line
                            # if grid block match with piece block and if is void or if is a motifs
                            if abs(x_piece - x_grid) < marg and abs(y_piece - y_grid) < marg and (self.grid.grid[y_g][x_g] == "NV" or (self.grid.grid[y_g][x_g][0] == "M" and self.current_piece.grid[y_p][x_p][1] == self.grid.grid[y_g][x_g][1])):
                                self.grid.grid[y_g][x_g] = self.current_piece.grid[y_p][x_p]
                                self.grid.grid_id[y_g][x_g] = self.new_id
                            elif abs(x_piece - x_grid) < marg and abs(y_piece - y_grid) < marg and self.grid.grid[y_g][x_g] == "TV":
                                self.grid.grid[y_g][x_g] = "M" + self.current_piece.grid[y_p][x_p][1]
                                pos = (self.grid.min_x+x_g*self.grid.size_line, self.grid.max_y-(y_g+1)*self.grid.size_line)
                                animation = HoleAnimation(color=self.current_piece.grid[y_p][x_p][1], animation_pos=pos)
                                ANIMATION_LIST.append(animation)
        self.remove_widget(self.current_piece)
        # Add score and generate new piece
        if self.id_level == 0:
            block_in_piece = 0
            for y in self.current_piece.grid:
                for x in y:
                    if x != "NV":
                        block_in_piece += 1
            self.score += int(sqrt((Pieces.increase_int+1)*2)*block_in_piece/2)
            self.score_label.text = str(self.score)
            grid = Pieces.random_piece()
            Pieces.increase()
            button = PieceButton(grid=grid)
            self.zone_piece.my_scroll_view.grid_piece.piece_button.append(button)
            self.zone_piece.my_scroll_view.grid_piece.add_widget(button)
        self.current_piece = None
    
    def save(self, redo=False):
        if self.id_level == 0:
            grid = copy.deepcopy(self.grid.grid)
            score = copy.deepcopy(self.score)
            grid_id = copy.deepcopy(self.grid.grid_id)
            pieces = []
            for piece in self.zone_piece.my_scroll_view.grid_piece.piece_button:
                pieces.append(piece.grid)
            if self.current_piece:
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
            if self.current_piece:
                pieces.append(self.current_piece.grid)
            self.saves.append({"grid":grid, "pieces":pieces, "grid_id":grid_id})
    
    def undo_save(self):
        grid = copy.deepcopy(self.grid.grid)
        grid_id = copy.deepcopy(self.grid.grid_id)
        pieces = []
        for piece in self.zone_piece.my_scroll_view.grid_piece.piece_button:
            pieces.append(piece.grid)
        if self.current_piece:
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
            for piece in self.zone_piece.my_scroll_view.grid_piece.piece_button:
                piece.reload = False
            self.zone_piece.my_scroll_view.grid_piece.clear_widgets()
            for piece in self.saves[-1]["pieces"]:
                button = PieceButton(grid=piece)
                self.zone_piece.my_scroll_view.grid_piece.piece_button.append(button)
                self.zone_piece.my_scroll_view.grid_piece.add_widget(button)
            self.score = self.saves[-1]["score"]
            self.score_label.text = str(self.score)
            self.saves.pop(-1)
        else:
            if self.current_piece:
                self.remove_current_piece()
                return
            self.undo_save()
            self.grid.grid = self.saves[-1]["grid"]
            self.grid.grid_id = self.saves[-1]["grid_id"]
            self.zone_piece.my_scroll_view.grid_piece.piece_button = []
            for piece in self.zone_piece.my_scroll_view.grid_piece.piece_button:
                piece.reload = False
            self.zone_piece.my_scroll_view.grid_piece.clear_widgets()
            for grid in self.saves[-1]["pieces"]:
                button = PieceButton(grid=grid)
                self.zone_piece.my_scroll_view.grid_piece.piece_button.append(button)
                self.zone_piece.my_scroll_view.grid_piece.add_widget(button)
            self.saves.pop(-1)
    
    def redo(self):
        if self.current_piece:
            self.remove_current_piece()
            return
        self.save(redo=True)
        self.grid.grid = copy.deepcopy(self.undo_saves[-1]["grid"])
        self.grid.grid_id = copy.deepcopy(self.undo_saves[-1]["grid_id"])
        self.zone_piece.my_scroll_view.grid_piece.piece_button = []
        for piece in self.zone_piece.my_scroll_view.grid_piece.piece_button:
            piece.reload = False
        self.zone_piece.my_scroll_view.grid_piece.clear_widgets()
        for grid in self.undo_saves[-1]["pieces"]:
            button = PieceButton(grid=grid)
            self.zone_piece.my_scroll_view.grid_piece.piece_button.append(button)
            self.zone_piece.my_scroll_view.grid_piece.add_widget(button)
        self.undo_saves.pop(-1)
    
    def change_current_piece(self, grid, pos, delta_pos):
        self.remove_current_piece()
        self.current_piece = CurrentPiece(grid=grid, size_line=self.grid.size_line, pos=pos, delta_pos=delta_pos)
        self.add_widget(self.current_piece)

    def not_reload(self):
        self.reload = False
        self.undo_button.reload = False
        self.menu_button.reload = False
        if self.score_label:
            self.score_label.reload = False
        if self.redo_button:
            self.redo_button.reload = False
        if self.current_piece:
            self.current_piece.reload = False
        if self.left_arrow:
            self.left_arrow.reload = False
        if self.right_arrow:
            self.right_arrow.reload = False
        self.grid.reload = False
        self.zone_piece.my_scroll_view.reload = False
        for button in self.zone_piece.my_scroll_view.grid_piece.piece_button:
            button.reload = False
    
    def remove_current_piece(self):
        if not self.current_piece:
            return
        self.remove_widget(self.current_piece)
        button = PieceButton(grid=self.current_piece.grid)
        self.zone_piece.my_scroll_view.grid_piece.piece_button.append(button)
        self.zone_piece.my_scroll_view.grid_piece.add_widget(button)
        self.current_piece = None
    
    def message_push(self):
        if not self.message:
            self.message = MenuMessage(score=self.score, id_level=self.id_level, mode=self.mode, temp_parent=self)
            self.add_widget(self.message)
    
    def message_pop(self):
        if self.message:
            self.remove_widget(self.message)
            self.message = None
    
    def verify(self):
        try:
            marg = int(self.grid.size_line/2)
            check = []
            for y_p in range(len(self.current_piece.grid)):
                for x_p in range(len(self.current_piece.grid[y_p])):
                    one = []
                    for y_g in range(len(self.grid.grid)):
                        for x_g in range(len(self.grid.grid[y_g])):
                            # Calculation Global of x and y for piece and grid
                            x_piece = self.current_piece.min_x+self.current_piece.x+x_p*self.current_piece.size_line
                            y_piece = self.current_piece.max_y+self.current_piece.y-(y_p+1)*self.current_piece.size_line
                            x_grid = self.grid.min_x+self.grid.x+x_g*self.grid.size_line
                            y_grid = self.grid.max_y+self.grid.y-(y_g+1)*self.grid.size_line
                            # if grid block match with piece block and if is void or if is a motis
                            one.append(abs(x_piece - x_grid) < marg and abs(y_piece - y_grid) < marg and (self.grid.grid[y_g][x_g] == "NV" or self.grid.grid[y_g][x_g] == "TV" or (self.grid.grid[y_g][x_g][0] == "M" and self.current_piece.grid[y_p][x_p][1] == self.grid.grid[y_g][x_g][1]) or self.current_piece.grid[y_p][x_p] == "NV"))
                    check.append(any(one))
            return all(check)
        except:
            return False


class Game(Screen):
    id_level = NumericProperty(None)
    my_float = ObjectProperty(None)
    page = ObjectProperty(None)
    
    def restart(self, id_level):
        if self.page:
            self.page.not_reload()
        self.clear_widgets()
        self.id_level = id_level
        # Reset Pieces
        Pieces.init()
        self.my_float = FloatLayout()
        if id_level == 0:
            self.mode = []
            self.arrows = True
            self.background = "assets/images/backgrounds/space.jpg"
        else:
            for area in Areas:
                for level in area["Levels"]:
                    if level["Id"] == self.id_level:
                        self.mode = level["Mode"]
                        self.background = area["Background"]
            self.arrows = 25 in self.mode
        self.page = Page(arrows=self.arrows, id_level=self.id_level, mode=self.mode)
        self.my_float.add_widget(Image(source=self.background, fit_mode="cover"))
        self.my_float.add_widget(self.page)
        self.add_widget(self.my_float)