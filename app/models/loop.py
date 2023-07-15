from kivy.clock import Clock

class Loop:
    def __init__(self) -> None:
        Clock.schedule_interval(self.loop, 1/60)
    
    def loop(self, *args):
        pass
