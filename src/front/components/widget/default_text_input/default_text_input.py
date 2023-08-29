from os import path

from kivymd.uix.textfield import MDTextField

from kivy.lang import Builder

Builder.load_file(path.join(path.dirname(__file__),"default_text_input.kv"))

class DefaultTextInput(MDTextField):
    pass
