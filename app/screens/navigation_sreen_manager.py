from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, ObjectProperty
from kivy.clock import Clock

from data import *
from screens.game_screen import Game


class TransitionScreen(Screen):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self.app = App.get_running_app()
    
    def on_enter(self, *args):
        Clock.schedule_once(self.app.manager.suivant, self.app.manager.delay/60)
        return super().on_enter(*args)


class NavigationScreenManager(ScreenManager):
    screen_stack = ListProperty([])
    transition = ObjectProperty(FadeTransition(duration=0.2))
    game = ObjectProperty(Game(name="Game"))
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.level = False
        self.add_widget(self.game)
    
    def on_touch_down(self, touch):
        # Disable the click event for all widget if click_disabled
        if App.get_running_app().click_disabled:
            return
        return super().on_touch_down(touch)

    def change_transition(self, transition_screen, screen_name) -> None:
        if transition_screen:
            self.transition = FadeTransition(duration=0.4)
            self.current = "TransitionScreen"
        else:
            self.transition = FadeTransition(duration=0)
            self.current = screen_name
    
    def push(self, screen_name, transition_screen=True, delay=0) -> None:
        self.delay = delay
        if screen_name not in self.screen_stack:
            self.screen_stack.append(self.current)
            self.change_transition(transition_screen, screen_name)
            self.next_current = screen_name

    def pop(self, transition_screen=True, delay=0, quit_level=False) -> None:
        self.delay = delay
        if len(self.screen_stack) > 0:
            screen_name = self.screen_stack[-1]
            del self.screen_stack[-1]
            self.change_transition(transition_screen, screen_name)
            self.next_current = screen_name
            if not quit_level:
                for screen in self.screens:
                    if screen.name == "StoryMode":
                        screen.children[0].children[0].message_pop()
    
    def start_level(self, id_level=0, transition_screen=True, delay=0) -> None:
        self.delay = delay
        if self.level:
            self.pop(transition_screen=transition_screen)
        self.level = True
        self.push(self.game.name, transition_screen=transition_screen)
        self.game.restart(id_level)

    def quit_level(self, transition_screen=True, delay=0) -> None:
        self.delay = delay
        if len(self.screen_stack) > 0:
            if self.game.id_level == 0:
                Settings.last_score = self.game.page.score
                b = False
                for s in Settings.best_score:
                    if self.game.page.score > s:
                        b = True
                if b:
                    best_score = list(Settings.best_score)
                    best_score.append(self.game.page.score)
                    sorted_list = list(sorted(best_score, reverse=True))
                    sorted_list.pop(-1)
                    Settings.best_score = sorted_list
            elif self.game.id_level != 0:
                if self.game.id_level + 1 == Settings.current_level:
                    for screen in self.screens:
                        if screen.name == "StoryMode":
                            screen.children[0].children[0].reset()
            self.pop(transition_screen=transition_screen, quit_level=True)
            self.level = False
    
    def suivant(self, *arg) -> None:
        if self.next_current:
            self.current = self.next_current