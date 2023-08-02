from os import path

from kivymd.uix.toolbar import MDTopAppBar

from kivy.lang import Builder

Builder.load_file(path.join(path.dirname(__file__),"main_app_bar.kv"))

class MainAppBar(MDTopAppBar):
    """
        Contain the main top bar of Riverapp
    """