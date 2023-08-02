from os import path

from kivymd.uix.button import MDIconButton
from kivy.properties import StringProperty
from kivy.lang import Builder

Builder.load_file(path.join(path.dirname(__file__),"text_under_icon_button.kv"))

class TextUnderIconButton(MDIconButton):
    text = StringProperty()
