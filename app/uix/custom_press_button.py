from kivy.uix.button import Button
from kivy.properties import NumericProperty


class CustomPressButton(Button):
    __last_press = False
    custom_press = NumericProperty(0)
    
    def on_press(self):
        self.__last_press = True
        return super().on_press()
    
    def on_touch_up(self, touch):
        if self.__last_press and self.collide_point(*touch.pos):
            self.custom_press += 1
        self.__last_press = False
        return super().on_touch_up(touch)

    def on_custom_press(self, *args):
        pass