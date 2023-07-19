from os import path

from kivymd.uix.dialog import MDDialog
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.utils import get_hex_from_color

Builder.load_file(path.join(path.dirname(__file__),"confirm_action.kv"))

class ConfirmAction(MDDialog):
    """
        Popup that appears to confirm that the user wishes to perform an action
    """
    cancel_text = StringProperty("Cancel")
    confirm_text = StringProperty()
    confirm_callback = ObjectProperty()
