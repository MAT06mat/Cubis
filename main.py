from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

from navigation_sreen_manager import NavigationScreenManager


class TransitionScreen(Screen):
    def on_enter(self, *args):
        app = App.get_running_app()
        app.manager.suivant()
        return super().on_enter(*args)


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