from kivymd.uix.dialog import MDDialog
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.utils import get_hex_from_color

from os import path

Builder.load_file(path.join(path.dirname(__file__),"confirm_action.kv"))

class ConfirmAction(MDDialog):
    cancel_text = StringProperty("Cancel")
    confirm_text = StringProperty()
    confirm_callback = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Dialog title & text color can only be changed by using kivy markup (https://kivy.org/doc/stable/api-kivy.core.text.markup.html)
        self.title = f"[color={get_hex_from_color(self.theme_cls.opposite_text_color)}]{self.title}[/color]"
        self.text = f"[color={get_hex_from_color(self.theme_cls.opposite_text_color)}]{self.text}[/color]"