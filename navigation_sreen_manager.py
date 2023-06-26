from kivy.uix.screenmanager import ScreenManager, FadeTransition


class NavigationScreenManager(ScreenManager):
    screen_stack = []
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
    
    def suivant(self):
        if self.next_current:
            self.current = self.next_current
