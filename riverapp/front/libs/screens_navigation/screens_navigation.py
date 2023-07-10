from kivymd.uix.navigationdrawer.navigationdrawer import MDNavigationLayout
from kivy.lang import Builder

from os import path

Builder.load_file(path.join(path.dirname(__file__),"screens_navigation.kv"))

class ScreensNavigation(MDNavigationLayout):
    pass