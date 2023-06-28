import json
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.clock import Clock
from kivy.metrics import dp

from message import PlayMessage

Builder.load_file("story_mode.kv")

with open("data.json") as data:
    DATA = json.load(data)
AREAS = DATA["Areas"]
CURRENT_LEVEL = DATA["Current_level"]
BACKGROUND_BASE = AREAS[0]["Background"]


class Level(Button):
    def __init__(self, level, **kwargs):
        super().__init__(**kwargs)
        # new var
        self.id = level["Id"]
        self.mode = level["Mode"]
        # define object
        self.text = str(self.id)
        if self.id > CURRENT_LEVEL:
            self.disabled = True
        
        # Mettre 0 devant les chiffres pour en faire des nombre à deux chiffres
        self.lines = []
        if len(self.text) == 1:
            self.text = "0" + self.text
        # if disabled : change style of button on disabled
        # if id%5 : change style of button on square
        if self.disabled:
            if self.id % 5 == 0:
                self.background_disabled_normal = "images/buttons/special_level_disabled.png"
            else:
                self.background_disabled_normal = "images/buttons/level_disabled.png"
            self.color = (1, 1, 1, 0)
        if self.id % 5 == 0:
            self.background_normal = "images/buttons/special_level.png"
            self.background_down = "images/buttons/special_level.png"
        
        # put 1/2 on top and 1/2 on bottom
        global level_height
        if level_height % 2 == 0:
            self.pos_hint = {"center_y": 0.70}
        else:
            self.pos_hint = {"center_y": 0.30}
        level_height += 1
        
    def on_press(self):
        self.parent.parent.parent.parent.parent.message_push(self.text, self.mode)
        return super().on_press()


class Area(BoxLayout):
    def __init__(self, levels, **kwargs):
        super().__init__(**kwargs)
        self.padding = dp(30)
        # define level and put the firt on bottom
        global level_height
        level_height = 1
        for level in levels:
            b = Level(level=level)
            self.add_widget(b)


class MyScrollView(ScrollView):
    def __init__(self, nb_levels, **kwargs):
        super().__init__(**kwargs)
        self.nb_levels = nb_levels
    
    def update_from_scroll(self, *largs):
        if tuto:
            background_image.children[0].pos_hint = {"x": 0}
        else:
            background_image.children[0].pos_hint = {"x": -self.scroll_x/100*self.nb_levels-0.25}
        return super().update_from_scroll(*largs)


class TabItem(TabbedPanelItem):
    def __init__(self, name, levels, image, **kwargs):
        super().__init__(**kwargs)
        self.text = name
        self.font_name = "fonts/Coda-Regular.ttf"
        self.image = image
        self.scroll_view = MyScrollView(nb_levels=len(levels))
        self.scroll_view.add_widget(Area(levels=levels))
        self.add_widget(self.scroll_view)
    
    def on_press(self):
        background_image.clear_widgets()
        background_image.add_widget(Image(source=self.image, fit_mode="cover", mipmap=True))
        global tuto
        if self.text == "Tutoriel":
            tuto = True
            background_image.size_hint = (1, 1)
        else:
            tuto = False
            background_image.size_hint = (4, 1)
        return super().on_press()
    

class StoryMode(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)

        # create tab item
        level = 0
        for area in AREAS:
            new_TabbedPanelItem = TabItem(name=area["Name"], levels=area["Levels"], image=area["Background"])
            if level < CURRENT_LEVEL:
                self.add_widget(new_TabbedPanelItem)
            level += len(area["Levels"])


class MyBackgroundImage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        self.add_widget(Image(source=BACKGROUND_BASE, fit_mode="cover"))


class StoryModeFloat(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.message = None

        global background_image, tuto
        tuto = True
        background_image = MyBackgroundImage()
        
        self.add_widget(background_image)
        self.add_widget(StoryMode())
        
    def message_push(self, text, mode):
        if not self.message:
            self.message = PlayMessage(text_var=text, mode=mode)
            self.add_widget(self.message)
        
    def message_pop(self):
        if self.message:
            self.remove_widget(self.message)
            self.message = None