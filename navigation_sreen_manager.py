from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, ListProperty, ObjectProperty

from story_game import StoryGame
from infinite_game import InfiniteGame
from data import SETTINGS


class TransitionScreen(Screen):
    def on_enter(self, *args):
        app = App.get_running_app()
        app.manager.suivant()
        return super().on_enter(*args)


class NavigationScreenManager(ScreenManager):
    screen_stack = ListProperty([])
    level = ObjectProperty(None)
    id = NumericProperty(0)
    transition = ObjectProperty(FadeTransition(duration=0.2))

    def change_transition(self, transition_screen, screen_name):
        if transition_screen:
            self.transition = FadeTransition(duration=0.4)
            self.current = "TransitionScreen"
        else:
            self.transition = FadeTransition(duration=0)
            self.current = screen_name
    
    def push(self, screen_name, transition_screen=True):
        if screen_name not in self.screen_stack:
            self.screen_stack.append(self.current)
            self.change_transition(transition_screen, screen_name)
            self.next_current = screen_name

    def pop(self, transition_screen=True):
        if len(self.screen_stack) > 0:
            screen_name = self.screen_stack[-1]
            del self.screen_stack[-1]
            self.change_transition(transition_screen, screen_name)
            self.next_current = screen_name
    
    def start_level(self, id_level=0):
        self.id += 1
        self.last_level = None
        if self.level != None:
            self.last_level = self.level
        name = "Level"+str(self.id)
        if id_level == 0:
            self.level = InfiniteGame(name=name)
        else:
            self.level = StoryGame(name=name, id_level=id_level)
        self.add_widget(self.level)
        self.push(name)
        if self.last_level != None:
            self.remove_widget(self.last_level)
            self.screen_stack.remove(self.last_level.name)
    
    def quit_level(self, transition_screen=True):
        if len(self.screen_stack) > 0:
            self.pop(transition_screen)
            try:
                test = self.level.id_level
            except AttributeError:
                SETTINGS.modify("Last_score", self.level.page.score)
                b = False
                for s in SETTINGS.get("Best_score"):
                    if self.level.page.score > s:
                        b = True
                if b:
                    best_score = list(SETTINGS.get("Best_score"))
                    best_score.append(self.level.page.score)
                    sorted_list = list(sorted(best_score, reverse=True))
                    sorted_list.pop(-1)
                    SETTINGS.modify("Best_score", sorted_list)
            self.level = None
    
    def suivant(self):
        if self.next_current:
            self.current = self.next_current
