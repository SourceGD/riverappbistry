from kivymd.uix.widget import MDWidget
from kivy.properties import NumericProperty, ColorProperty, BooleanProperty
from kivy.lang import Builder
from kivy.graphics import Color, Ellipse

from os import path

Builder.load_file(path.join(path.dirname(__file__),"reverse_lollipop.kv"))

class ReverseLollipop(MDWidget):
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
        if not self.canvas:
            return None
        
        if value:
            with self.canvas.after:
                Color(rgba=self.active_color)
                Ellipse(
                    pos=(
                        self.x + self.width / 2 * 0.3375,
                        self.y + self.width / 2 * 0.3375 + self.height * (self.order - 1)
                    ),
                    size=(self.width / 2 * 1.35, self.width / 2 * 1.35)
                )

        else:
            self.canvas.after.clear()
            
        self.canvas.ask_update()
