from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.uix.screenmanager import Screen

from story_game import StoryGame
from infinite_game import InfiniteGame

import json


class TransitionScreen(Screen):
    def on_enter(self, *args):
        app = App.get_running_app()
        app.manager.suivant()
        return super().on_enter(*args)


class NavigationScreenManager(ScreenManager):
    screen_stack = []
    level = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = 0
        self.transition = FadeTransition(duration=0.5)

    def push(self, screen_name, transition_screen=True):
        if screen_name not in self.screen_stack:
            self.screen_stack.append(self.current)
            if transition_screen:
                self.transition = FadeTransition(duration=0.5)
                self.current = "TransitionScreen"
            else:
                self.transition = FadeTransition(duration=0)
                self.current = screen_name
            self.next_current = screen_name

    def pop(self, transition_screen=True):
        if len(self.screen_stack) > 0:
            screen_name = self.screen_stack[-1]
            del self.screen_stack[-1]
            if transition_screen:
                self.transition = FadeTransition(duration=0.5)
                self.current = "TransitionScreen"
            else:
                self.transition = FadeTransition(duration=0)
                self.current = screen_name
            self.next_current = screen_name
    
    def start_level(self, id_level=0):
        self.id += 1
        self.last_level = None
        if self.level != None:
            self.last_level = self.level
        if id_level == 0:
            self.level = InfiniteGame(name="Level"+str(self.id))
        else:
            self.level = StoryGame(name="Level"+str(self.id), id_level=id_level)
        self.add_widget(self.level)
        self.push("Level"+str(self.id))
        if self.last_level != None:
            self.remove_widget(self.last_level)
            self.screen_stack.remove(self.last_level.name)
    
    def quit_level(self, transition_screen=True):
        if len(self.screen_stack) > 0:
            screen_name = self.screen_stack[-1]
            del self.screen_stack[-1]
            if transition_screen:
                self.transition = FadeTransition(duration=0.5)
                self.current = "TransitionScreen"
            else:
                self.transition = FadeTransition(duration=0)
                self.current = screen_name
            self.next_current = screen_name
            try:
                test = self.level.id_level
            except AttributeError:
                with open("data.json", "r") as file:
                    data = json.load(file)
                data["Last_score"] = self.level.page.score
                b = False
                for s in data["Best_score"]:
                    if self.level.page.score > s:
                        b = True
                if b:
                    best_score = list(data["Best_score"])
                    best_score.append(self.level.page.score)
                    sorted_list = list(sorted(best_score, reverse=True))
                    sorted_list.pop(-1)
                    data["Best_score"] = sorted_list
                with open("data.json", "w") as file:
                    file.write(json.dumps(data))
            self.level = None
    
    def suivant(self):
        if self.next_current:
            self.current = self.next_current
