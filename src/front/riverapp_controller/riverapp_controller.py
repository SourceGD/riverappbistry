from os import path

from kivymd.uix.navigationdrawer.navigationdrawer import MDNavigationLayout
from kivy.lang import Builder

Builder.load_file(path.join(path.dirname(__file__),"riverapp_controller.kv"))

class RiverappController(MDNavigationLayout):
    """
        This class may be deleted in the future if no special methods is needed
    """
