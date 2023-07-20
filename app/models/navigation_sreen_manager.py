from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, ObjectProperty

from models.loop import Loop
from controllers.game_manager import Game
from models.data import SETTINGS


class TransitionScreen(Screen, Loop):
    delay = None
    timer = 0
    
    def on_enter(self, *args):
        app = App.get_running_app()
        if app.manager.delay == 0:
            app.manager.suivant()
        else:
            self.delay = app.manager.delay
        return super().on_enter(*args)

    def loop(self, *args):
        if self.delay:
            self.timer += 1
            if self.timer > self.delay:
                app = App.get_running_app()
                app.manager.suivant()
                self.delay = None
        else:
            self.timer = 0
            
        


class NavigationScreenManager(ScreenManager):
    screen_stack = ListProperty([])
    transition = ObjectProperty(FadeTransition(duration=0.2))
    game = ObjectProperty(Game(name="Game"))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level = False
        self.add_widget(self.game)

    def change_transition(self, transition_screen, screen_name):
        if transition_screen:
            self.transition = FadeTransition(duration=0.4)
            self.current = "TransitionScreen"
        else:
            self.transition = FadeTransition(duration=0)
            self.current = screen_name
    
    def push(self, screen_name, transition_screen=True, delay=0):
        self.delay = delay
        if screen_name not in self.screen_stack:
            self.screen_stack.append(self.current)
            self.change_transition(transition_screen, screen_name)
            self.next_current = screen_name

    def pop(self, transition_screen=True, delay=0):
        self.delay = delay
        if len(self.screen_stack) > 0:
            screen_name = self.screen_stack[-1]
            del self.screen_stack[-1]
            self.change_transition(transition_screen, screen_name)
            self.next_current = screen_name
    
    def start_level(self, id_level=0, transition_screen=True, delay=0):
        self.delay = delay
        if self.level:
            self.pop(transition_screen=transition_screen)
        self.level = True
        self.push(self.game.name, transition_screen=transition_screen)
        self.game.restart(id_level)

    def quit_level(self, transition_screen=True, delay=0, victoire=False):
        self.delay = delay
        if len(self.screen_stack) > 0:
            if self.game.id_level == 0:
                SETTINGS.modify(element=self.game.page.score, key="Last_score")
                b = False
                for s in SETTINGS.get()["Best_score"]:
                    if self.game.page.score > s:
                        b = True
                if b:
                    best_score = list(SETTINGS.get()["Best_score"])
                    best_score.append(self.game.page.score)
                    sorted_list = list(sorted(best_score, reverse=True))
                    sorted_list.pop(-1)
                    SETTINGS.modify(element=sorted_list, key="Best_score")
            elif self.game.id_level != 0:
                current_level = SETTINGS.get()["Current_level"]
                if self.game.id_level == current_level and victoire:
                    SETTINGS.modify(element=current_level+1, key="Current_level")
                    for screen in self.screens:
                        if screen.name == "StoryMode":
                            screen.children[0].children[0].reset()
            self.pop(transition_screen=transition_screen)
            self.level = False
            
    def suivant(self):
        if self.next_current:
            self.current = self.next_current
