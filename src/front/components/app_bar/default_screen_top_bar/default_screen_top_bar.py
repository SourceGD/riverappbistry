from os import path

from kivymd.uix.boxlayout import MDBoxLayout

from kivy.properties import ListProperty, StringProperty, BooleanProperty, ObjectProperty
from kivy.lang import Builder

Builder.load_file(path.join(path.dirname(__file__),"default_screen_top_bar.kv"))

class DefaultScreenTopBar(MDBoxLayout):
    """
        Top Screen content which is the App Name Bar
        and the Screen Title bar
    """
    left_action_items = ListProperty()
    right_action_items = ListProperty()
    title = StringProperty()
    use_overflow = BooleanProperty(False)
    overflow_cls = ObjectProperty()