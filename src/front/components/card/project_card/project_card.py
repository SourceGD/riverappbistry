from os import path

from kivymd.uix.card import MDCard

from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder

Builder.load_file(path.join(path.dirname(__file__),"project_card.kv"))

class ProjectCard(MDCard):
    
    title: StringProperty = StringProperty()
    delete_callback: ObjectProperty = ObjectProperty()
    download_callback: ObjectProperty = ObjectProperty()


