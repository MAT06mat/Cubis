from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.core.window import Window

from app.controllers.navigation_sreen_manager import NavigationScreenManager

class MyScreenManager(NavigationScreenManager):
    pass


class CubisApp(App):
    manager = ObjectProperty(None)
    icon = "images/app/logo.png"
    
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        self.manager = MyScreenManager()
        return self.manager


CubisApp().run()