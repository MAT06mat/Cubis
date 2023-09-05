from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.properties import NumericProperty, ListProperty, StringProperty, ObjectProperty, DictProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

from models.loop import Loop
from models.background_image import MyBackgroundImage
from models.data import SETTINGS, AREAS, TEXTS
from controllers.message import PlayMessage, InfoMessage

import os

current_directory = os.path.dirname(os.path.realpath(__file__))
kv_file_path = os.path.join(current_directory, "../views/story_mode.kv")
Builder.load_file(kv_file_path)


global tuto
tuto = True
BACKGROUND_IMAGE = MyBackgroundImage()


class Level(Button):
    level = DictProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = self.level["Id"]
        self.mode = self.level["Mode"]
        self.text = str(self.id)
        if self.id > SETTINGS.get()["Current_level"]:
            self.disabled = True
        # Mettre 0 devant les chiffres pour en faire des nombre à deux chiffres
        self.lines = []
        if len(self.text) == 1:
            self.text = "0" + self.text
        # if disabled : change style of button on disabled
        # if id%5 : change style of button on square
        if self.disabled:
            if self.id % 5 == 0:
                self.background_disabled_normal = "assets/images/buttons/special_level_disabled.png"
            else:
                self.background_disabled_normal = "assets/images/buttons/level_disabled.png"
            self.color = (1, 1, 1, 0)
        if self.id % 5 == 0:
            self.background_normal = "assets/images/buttons/special_level.png"
            self.background_down = "assets/images/buttons/special_level.png"
        
        # put 1/2 on top and 1/2 on bottom
        global level_height
        if level_height % 2 == 0:
            self.pos_hint = {"center_y": 0.65}
        else:
            self.pos_hint = {"center_y": 0.35}
        level_height += 1
        
    def on_press(self):
        self.parent.parent.parent.parent.parent.message_push(self.id)
        return super().on_press()


class Area(BoxLayout):
    levels = ListProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # define level and put the firt on bottom
        global level_height
        level_height = 1
        for level in self.levels:
            b = Level(level=level)
            self.add_widget(b)


class MyScrollView(ScrollView):
    nb_levels = NumericProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bar_width = 0
    
    def update_from_scroll(self, *largs):
        if tuto:
            BACKGROUND_IMAGE.children[0].pos_hint = {"x": 0}
        else:
            BACKGROUND_IMAGE.children[0].pos_hint = {"x": -self.scroll_x/50*self.nb_levels-0.25} # Modified /50   |   /100 Default
        return super().update_from_scroll(*largs)


class TabItem(TabbedPanelItem):
    levels = ListProperty(None)
    image = StringProperty(None)
    
    def __init__(self, text_key, **kwargs):
        super().__init__(**kwargs)
        self.text_key = text_key
        self.scroll_view = MyScrollView(nb_levels=len(self.levels))
        self.scroll_view.add_widget(Area(levels=self.levels))
        self.add_widget(self.scroll_view)
        self.lang_change()
        TEXTS.bind(current_lang=self.lang_change)
        self.bind(disabled=self.text_change)
    
    def lang_change(self, *args):
        self.text_change()
        
    def text_change(self, *args):
        if self.disabled:
            self.text = "???"
        else:
            self.text = TEXTS.key(self.text_key)
    
    def on_press(self, pop=True):
        if self.parent.parent and pop:
            self.parent.parent.parent.parent.parent.message_pop()
        BACKGROUND_IMAGE.clear_widgets()
        BACKGROUND_IMAGE.add_widget(Image(source=self.image, fit_mode="cover", mipmap=True))
        global tuto
        if self.text == "Tutoriel":
            tuto = True
            BACKGROUND_IMAGE.size_hint = (1, 1)
        else:
            tuto = False
            BACKGROUND_IMAGE.size_hint = (4, 1)
        return super().on_press()


class StoryMode(TabbedPanel, Loop):
    level = NumericProperty(0)
    in_select_first_tab = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # create tab item
        self.bar_width = 0
        for area in AREAS.get():
            new_TabbedPanelItem = TabItem(text_key=area["Name"], levels=area["Levels"], image=area["Background"], disabled=True)
            self.add_widget(new_TabbedPanelItem)
            if self.level < SETTINGS.get()["Current_level"]:
                new_TabbedPanelItem.disabled = False
            self.level += len(area["Levels"])
        # Wait the loop in top is end
        Clock.schedule_once(self.select_first_tab, 0)
        
    def select_first_tab(self, dt):
        if self.tab_list:
            for tab in self.tab_list[:-1]:
                if tab.disabled == False:
                    self.switch_to(tab)
                    tab.on_press(pop=False)
                    return
    
    def loop(self, *args):
        for tab in self.tab_list:
            tab.color = "#F3E2DB"
        self.current_tab.color = "#FFFFFF"


class StoryModeFloat(FloatLayout):
    message = None
    story_mode = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        SETTINGS.bind(is_init=self.init)
    
    def init(self, *args):
        self.add_widget(BACKGROUND_IMAGE)
        self.story_mode = StoryMode()
        self.add_widget(self.story_mode)
    
    def reset(self):
        self.clear_widgets()
        self.add_widget(BACKGROUND_IMAGE)
        self.story_mode = StoryMode()
        self.add_widget(self.story_mode)
        message = False
        for area in AREAS.get():
            if SETTINGS.get()["Current_level"] == area["Levels"][0]["Id"]:
                self.message_pop()
                self.message = InfoMessage(message=[TEXTS.key(17)+TEXTS.key(area["Name"])], title=TEXTS.key(18))
                self.add_widget(self.message)
                message = True
        if not message:
            self.message_pop()
            self.message_push(SETTINGS.get()["Current_level"])
        
    def message_push(self, id_level):
        if not self.message: 
            level_exist = []
            for area in AREAS.get():
                for level in area["Levels"]:
                    level_exist.append(level["Id"] == id_level)
            if not any(level_exist):
                self.message = InfoMessage(message=TEXTS.key(20))
                self.add_widget(self.message)
            else:
                self.message = PlayMessage(id_level=id_level)
                self.add_widget(self.message)
        
    def message_pop(self):
        if self.message:
            self.remove_widget(self.message)
            self.message = None