from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty

from models.decorators import *
from models.loop import Loop
from uix.custom_press_button import CustomPressButton


class CustomResizeButton(CustomPressButton, Loop):
    __touch_inside = False
    __last_press = False
    coef_size = NumericProperty(170)
    source = StringProperty('')
    disabled_source = StringProperty('')
    custom_press = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (1, 1, 1, 0)
        self.image = Image(source=self.source, size=self.size, pos=self.pos)
        self.add_widget(self.image)
        self.bind(source=self.source_change, disabled_source=self.source_change, disabled=self.source_change)
        self.bind(size=self.update_image, coef_size=self.update_image, center=self.update_image)
        self.anim = Animation(d=0.1, t="in_out_quad", coef_size=170)
        self.anim_reverse = Animation(d=0.1, t="in_out_quad", coef_size=160)
    
    def source_change(self, *args):
        if self.disabled:
            self.image.source = self.disabled_source
        else:
            self.image.source = self.source
    
    def update_image(self, *args):
        self.image.size = (self.size[0]*self.coef_size/200, self.size[1]*self.coef_size/200)
        self.image.center = self.center
    
    def on_press(self):
        if not self.condition():
            return super().on_press()
        self.__last_press = True
        self.__touch_inside = True
        self.anim.cancel(self)
        self.anim_reverse.start(self)
        return super().on_press()
    
    def on_touch_move(self, touch):
        if self.__last_press and self.collide_point(*touch.pos) and not self.__touch_inside:
            self.__touch_inside = True
            self.anim.cancel(self)
            self.anim_reverse.start(self)
        elif self.__last_press and not self.collide_point(*touch.pos) and self.__touch_inside:
            self.__touch_inside = False
            self.anim.start(self)
            self.anim_reverse.cancel(self)
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        self.anim.start(self)
        self.anim_reverse.cancel(self)
        return super().on_touch_up(touch)