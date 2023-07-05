from kivymd.uix.dialog import MDDialog
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from os import path

Builder.load_file(path.join(path.dirname(__file__),"confirm_action.kv"))

class ConfirmAction(MDDialog):
    cancel_text = StringProperty("Cancel")
    confirm_text = StringProperty()
    confirm_callback = ObjectProperty()

    

