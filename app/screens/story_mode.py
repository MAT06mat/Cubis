from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.properties import NumericProperty, ListProperty, StringProperty, ObjectProperty, DictProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
from kivy.clock import Clock

from data.settings import Settings
from data.areas import Areas
from data.texts import Texts
from models.loop import Loop
from models.message import PlayMessage, InfoMessage
from uix.background_image import MyBackgroundImage


Builder.load_file("screens/story_mode.kv")


global tuto
tuto = True
BACKGROUND_IMAGE = MyBackgroundImage()


class Level(Button):
    level = DictProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = self.level["Id"]
        self.mode = self.level["Mode"]
        self.size = (dp(125), dp(125))
        if self.id > Settings.current_level:
            self.disabled = True
            self.color = (1, 1, 1, 0)
        # Mettre 0 devant les chiffres pour en faire des nombre à deux chiffres
        self.text = str(self.id)
        while len(self.text) < 2:
            self.text = "0" + self.text
        # if disabled : change style of button on disabled
        # if id%5 : change style of button on square
        if self.id % 5 == 0:
            self.background_disabled_normal = "assets/images/buttons/special_level_disabled.png"
        else:
            self.background_disabled_normal = "assets/images/buttons/level_disabled.png"
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
    
    def reset(self):
        if self.id <= Settings.current_level:
            self.disabled = False
            self.color = "#A04623"
        else:
            self.color = (1, 1, 1, 0)
        
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
    current = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bar_width = 0
        self.update()
    
    def update_from_scroll(self, *largs):
        if self.current:
            self.update()
        return super().update_from_scroll(*largs)
    
    def update(self):
        if tuto:
            BACKGROUND_IMAGE.children[0].pos_hint = {"x": 0}
        else:
            BACKGROUND_IMAGE.children[0].pos_hint = {"x": -self.scroll_x/50*self.nb_levels-0.25} # Modified /50   |   /100 Default


class TabItem(TabbedPanelItem):
    levels = ListProperty(None)
    image = StringProperty(None)
    
    def __init__(self, text_key, **kwargs):
        super().__init__(**kwargs)
        self.text_key = text_key
        self.scroll_view = MyScrollView(nb_levels=len(self.levels))
        self.area = Area(levels=self.levels)
        self.scroll_view.add_widget(self.area)
        self.add_widget(self.scroll_view)
        self.lang_change()
        Texts.bind(current_lang=self.lang_change)
        self.bind(disabled=self.text_change)
    
    def lang_change(self, *args):
        self.text_change()
        
    def text_change(self, *args):
        if self.disabled:
            self.text = "???"
        else:
            self.text = Texts.key(self.text_key)
    
    def reset(self):
        current_level = Settings.current_level
        for level in self.area.children:
            level.reset()
        for level in self.levels:
            if level["Id"] <= current_level:
                self.disabled = False
            if level["Id"] == current_level:
                self.on_press()
    
    def on_press(self, pop=True):
        if self.parent.parent and pop:
            self.parent.parent.parent.parent.parent.message_pop()
        BACKGROUND_IMAGE.clear_widgets()
        BACKGROUND_IMAGE.add_widget(Image(source=self.image, fit_mode="cover", mipmap=True))
        global tuto
        if self.text_key == 15:
            tuto = True
            BACKGROUND_IMAGE.size_hint = (1, 1)
        else:
            tuto = False
            BACKGROUND_IMAGE.size_hint = (4, 1)
        if self.parent.parent:
            self.parent.parent.parent.parent.stop_every_scroll()
        self.scroll_view.current = True
        self.scroll_view.update()
        return super().on_press()


class StoryMode(TabbedPanel, Loop):
    level = NumericProperty(1)
    tabs = []
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # create tab item
        self.bar_width = 0
        for area in Areas.get():
            new_TabbedPanelItem = TabItem(text_key=area["Name"], levels=area["Levels"], image=area["Background"], disabled=True)
            self.add_widget(new_TabbedPanelItem)
            self.tabs.append(new_TabbedPanelItem)
            if self.level <= Settings.current_level:
                new_TabbedPanelItem.disabled = False
            self.level += len(area["Levels"])
        # Wait the loop in top is end
        Clock.schedule_once(self.select_first_tab)

    def reset(self):
        for area in self.tabs:
            area.reset()
        self.select_first_tab()
    
    def select_first_tab(self, *args):
        if self.tab_list:
            self.stop_every_scroll()
            for tab in self.tab_list[:-1]:
                if tab.disabled == False:
                    self.switch_to(tab)
                    tab.on_press(pop=False)
                    return
    
    def stop_every_scroll(self):
        for tab in self.tab_list:
            tab.scroll_view.current = False
    
    def loop(self, *args):
        for tab in self.tab_list:
            tab.color = "#F6DBCF"
        self.current_tab.color = "#FFFFFF"


class StoryModeFloat(FloatLayout):
    message = None
    story_mode = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Settings.bind(is_init=self.init)
    
    def init(self, *args):
        self.add_widget(BACKGROUND_IMAGE)
        self.story_mode = StoryMode()
        self.add_widget(self.story_mode)
    
    def reset(self):
        self.clear_widgets()
        self.add_widget(BACKGROUND_IMAGE)
        self.add_widget(self.story_mode)
        self.story_mode.reset()
        message = False
        for area in Areas.get():
            if Settings.current_level == area["Levels"][0]["Id"]:
                self.message_pop()
                self.message = InfoMessage(message=[Texts.key(17)+Texts.key(area["Name"])], title=Texts.key(18))
                self.add_widget(self.message)
                message = True
        if not message:
            self.message_pop()
            self.message_push(Settings.current_level)

    def message_push(self, id_level):
        if not self.message: 
            level_exist = []
            for area in Areas.get():
                for level in area["Levels"]:
                    level_exist.append(level["Id"] == id_level)
            if not any(level_exist):
                self.message = InfoMessage(message=Texts.key(20))
                self.add_widget(self.message)
            else:
                self.message = PlayMessage(id_level=id_level)
                self.add_widget(self.message)
        
    def message_pop(self):
        if self.message:
            self.remove_widget(self.message)
            self.message = None