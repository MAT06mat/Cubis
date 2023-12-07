from kivy.clock import Clock
from kivy.properties import BooleanProperty

class Loop:
    reload = BooleanProperty(True)
    
    def __init__(self) -> None:
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        return self.reload
