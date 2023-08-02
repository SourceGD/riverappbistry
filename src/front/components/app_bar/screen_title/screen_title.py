from os import path

from kivymd.uix.toolbar import MDTopAppBar

from kivy.lang import Builder

Builder.load_file(path.join(path.dirname(__file__),"screen_title.kv"))

class ScreenTitle(MDTopAppBar):
    """
        Contain the top app bar of the current page
    """