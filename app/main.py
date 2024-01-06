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
    debug = False
    
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        self.manager = MyScreenManager()
        return self.manager

    def on_start(self):
        Settings.init_with_user_data_dir(self.user_data_dir)
        for screen in self.manager.screens:
            if screen.name == "StartScreen":
                screen.children[0].ids["start_label"].start()
                screen.children[0].ids["start_button"].start()


if __name__ == '__main__':
    CubisApp().run()