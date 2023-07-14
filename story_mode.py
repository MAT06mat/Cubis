from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.properties import NumericProperty, ListProperty, StringProperty, ObjectProperty, DictProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

from message import PlayMessage, InfoMessage
from data import SETTINGS, AREAS

Builder.load_file("story_mode.kv")


class Level(Button):
    level = DictProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = self.level["Id"]
        self.mode = self.level["Mode"]
        self.text = str(self.id)
        if self.id > SETTINGS.get("Current_level"):
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
    
    def update_from_scroll(self, *largs):
        if tuto:
            background_image.children[0].pos_hint = {"x": 0}
        else:
            background_image.children[0].pos_hint = {"x": -self.scroll_x/100*self.nb_levels-0.25}
        return super().update_from_scroll(*largs)


class TabItem(TabbedPanelItem):
    levels = ListProperty(None)
    image = StringProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll_view = MyScrollView(nb_levels=len(self.levels))
        self.scroll_view.add_widget(Area(levels=self.levels))
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
    level = NumericProperty(0)
    tabs = ListProperty([])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # create tab item
        for area in AREAS.get("all"):
            new_TabbedPanelItem = TabItem(text=area["Name"], levels=area["Levels"], image=area["Background"])
            self.tabs.append(new_TabbedPanelItem)
            if self.level < SETTINGS.get("Current_level"):
                self.add_widget(new_TabbedPanelItem)
            self.level += len(area["Levels"])
        # Wait the loop in top is end
        Clock.schedule_once(self.change_tab, 0.1)
        Clock.schedule_interval(self.loop, 1/60)
    
    def change_tab(self, dt):
        for area in AREAS.get("all"):
            for level in area["Levels"]:
                for tab in self.tabs:
                    if SETTINGS.get("Current_level") == level["Id"] and area["Name"] == tab.text:
                        self.switch_to(tab)
                        tab.on_press()
    
    def loop(self, *args):
        for tab in self.tabs:
            tab.color = "#FFFFFF"
        self.current_tab.color = "#F3E2DB"


class MyBackgroundImage(FloatLayout):
    pass


class StoryModeFloat(FloatLayout):
    message = None
    story_mode = ObjectProperty(StoryMode())
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global background_image, tuto
        tuto = True
        background_image = MyBackgroundImage()
        self.add_widget(background_image)
        self.add_widget(self.story_mode)
    
    def reset(self):
        self.remove_widget(self.story_mode)
        self.story_mode = StoryMode()
        self.add_widget(self.story_mode)
        message = False
        for area in AREAS.get("all"):
            if SETTINGS.get("Current_level") == area["Levels"][0]["Id"]:
                self.message_pop()
                self.message = InfoMessage(message=("Nouvelle zone débloqué !"," Nouvelle zone : "+area["Name"]), title="Information")
                self.add_widget(self.message)
                message = True
        if not message:
            self.message_pop()
            self.message_push(SETTINGS.get("Current_level"))
        
    def message_push(self, id_level):
        if not self.message:
            self.message = PlayMessage(id_level=id_level)
            self.add_widget(self.message)
        
    def message_pop(self):
        if self.message:
            self.remove_widget(self.message)
            self.message = None