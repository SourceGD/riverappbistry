from os import path

from kivymd.uix.widget import MDWidget
from kivy.properties import NumericProperty, ColorProperty, BooleanProperty
from kivy.lang import Builder

Builder.load_file(path.join(path.dirname(__file__),"reverse_lollipop.kv"))

class ReverseLollipop(MDWidget):
    """
        Widget containing an inverted lollipop graphic design. 
        You can make a ball appear inside the lollipop.
    """
    order = NumericProperty(1)
    lollipop_color = ColorProperty("#FFFFFF")
    active_color = ColorProperty("#F27438")
    active = BooleanProperty(False)

    def on_order(self, instance, value: int | float) -> None:
        """ 
            Numeric property allows float and int but in this case we only want int value
        """
        if not isinstance(value, int):
            raise ValueError(f"order must be an int: {value}")

    def on_active(self, instance, value: bool) -> None:
        """
            Update the canvas when the active state change
        """
        self.canvas.ask_update()
