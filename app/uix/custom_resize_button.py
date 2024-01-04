from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty

from models.loop import Loop
from uix.custom_press_button import CustomPressButton


class CustomResizeButton(CustomPressButton, Loop):
    touch_inside = False
    """`Private var`"""
    
    last_press = False
    """`Private var`"""
    
    coef_size = NumericProperty(0)
    """`Private var`"""
    
    source = StringProperty('')
    '''Filename / source of your enabled button.

    :attr:`source` is a :class:`~kivy.properties.StringProperty` and
    defaults to None.
    '''
    
    disabled_source = StringProperty('')
    '''Filename / source of your disabled button.

    :attr:`disabled_source` is a :class:`~kivy.properties.StringProperty` and
    defaults to None.
    '''
    
    custom_press = NumericProperty(0)
    '''Event callback property / Property for call `on_custom_press` func.

    :attr:`custom_press` is an :class:`~kivy.properties.NumericProperty` and is
    read-only.
    '''
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (1, 1, 1, 0)
        self.image = Image(source=self.source, size=self.size, pos=self.pos)
        self.add_widget(self.image, canvas="before")
        self.bind(source=self._source_change, disabled_source=self._source_change, disabled=self._source_change)
        self.bind(size=self._update_image, coef_size=self._update_image, center=self._update_image)
        self.anim = Animation(d=0.1, t="in_out_quad", coef_size=0)
        self.anim_reverse = Animation(d=0.1, t="in_out_quad", coef_size=0.1)
    
    def _source_change(self, *args):
        if self.disabled:
            self.image.source = self.disabled_source
        else:
            self.image.source = self.source
    
    def _update_image(self, *args):
        self.image.size = (self.size[0]*(1-self.coef_size), self.size[1]*(1-self.coef_size))
        self.image.center = self.center
    
    def on_press(self):
        if not self.condition():
            return super().on_press()
        self.last_press = True
        self.touch_inside = True
        self.anim.cancel(self)
        self.anim_reverse.start(self)
        return super().on_press()
    
    def on_touch_move(self, touch):
        if self.last_press and self.collide_point(*touch.pos) and not self.touch_inside:
            self.touch_inside = True
            self.anim.cancel(self)
            self.anim_reverse.start(self)
        elif self.last_press and not self.collide_point(*touch.pos) and self.touch_inside:
            self.touch_inside = False
            self.anim.start(self)
            self.anim_reverse.cancel(self)
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        if self.last_press:
            self.anim.start(self)
            self.anim_reverse.cancel(self)
        return super().on_touch_up(touch)