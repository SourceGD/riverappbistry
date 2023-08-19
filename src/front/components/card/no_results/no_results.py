from os import path

from kivymd.uix.card import MDCard

from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder

Builder.load_file(path.join(path.dirname(__file__),"no_results.kv"))

class NoResults(MDCard):
    title: StringProperty = StringProperty()
    text: StringProperty = StringProperty()
