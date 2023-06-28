from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

from game import Game
from navigation_sreen_manager import NavigationScreenManager

# Exemple open data
"""with open("data.json", "r") as data:
    data_open = json.loads(data.read())
    data_open["Best_score"] += 1

with open("data.json", "w") as data:
    data.write(json.dumps(data_open))""" 


class TransitionScreen(Screen):
    def on_enter(self, *args):
        app = App.get_running_app()
        app.manager.suivant()
        return super().on_enter(*args)


class MyScreenManager(NavigationScreenManager):
    level = None

    def start_level(self, id_level=0):
        if self.level != None:
            self.remove_widget(self.level)
        self.level = Game(name="Level", id_level=id_level)
        self.add_widget(self.level)
        self.push("Level")


class CubisApp(App):
    manager = ObjectProperty(None)
    icon = "images/app/logo.png"
    
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        self.manager = MyScreenManager()
        return self.manager
        return Game(name="Level", id_level=5)


CubisApp().run()