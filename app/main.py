from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.core.window import Window

from screens.navigation_sreen_manager import NavigationScreenManager
from data import *

class MyScreenManager(NavigationScreenManager):
    pass


class CubisApp(App):
    click_disabled = False
    manager = ObjectProperty(None)
    icon = "assets/images/app/logo.png"
    
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        self.manager = MyScreenManager()
        return self.manager

    def on_start(self):
        Settings.init_with_user_data_dir(self.user_data_dir)


if __name__ == '__main__':
    CubisApp().run()