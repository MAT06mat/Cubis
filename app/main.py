from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.clock import Clock

from models.navigation_sreen_manager import NavigationScreenManager
from models.data import SETTINGS

class MyScreenManager(NavigationScreenManager):
    pass


class CubisApp(App):
    manager = ObjectProperty(None)
    icon = "assets/images/app/logo.png"
    
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        self.manager = MyScreenManager()
        return self.manager

    def on_start(self):
        SETTINGS.init_with_user_data_dir(self.user_data_dir)
    

CubisApp().run()