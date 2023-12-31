from uix.custom_press_button import CustomPressButton
from kivy.lang import Builder


Builder.load_file("uix/custom_button.kv")


class CustomButton(CustomPressButton):
    pass