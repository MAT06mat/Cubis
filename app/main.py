from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.core.window import Window

from models.navigation_sreen_manager import NavigationScreenManager

class MyScreenManager(NavigationScreenManager):
    pass


class CubisApp(App):
    manager = ObjectProperty(None)
    icon = "assets/images/app/logo.png"
    
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        self.manager = MyScreenManager()
        return self.manager


CubisApp().run()