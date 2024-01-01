from kivy.uix.button import Button
from kivy.properties import NumericProperty, BooleanProperty
from kivy.clock import Clock
from kivy.app import App


class CustomPressButton(Button):
    last_press = False
    """`Private var`"""
    
    custom_press = NumericProperty(0)
    '''Event callback property / Property for call `on_custom_press` func.

    :attr:`custom_press` is an :class:`~kivy.properties.NumericProperty` and is
    read-only.
    '''
    
    wait_end = BooleanProperty(False)
    '''Indicate if you want wait the end of the animation for call :func:`on_custom_press` func (mouse is disabled on this time).

    :attr:`wait_end` is a :class:`~kivy.properties.BooleanProperty` and defaults
    to False.
    '''
    
    def on_press(self):
        if not self.condition():
            return super().on_press()

        self.last_press = True
        return super().on_press()
    
    def on_touch_up(self, touch):
        if self.last_press and self.collide_point(*touch.pos):
            
            def callback(*args):
                App.get_running_app().click_disabled = False
                self.custom_press += 1
            
            if self.wait_end:
                # Wait the end of the animation
                Clock.schedule_once(callback, 0.11)
                App.get_running_app().click_disabled = True
            else:
                callback()
        
        self.last_press = False
        return super().on_touch_up(touch)
    
    def condition(self):
        """Condition for start animation on the `on_press` event and call `on_custom_press` func.
        `Default: return True`"""
        return True
    
    def on_custom_press(self, *args):
        """Custom press event, call after unclick the button"""