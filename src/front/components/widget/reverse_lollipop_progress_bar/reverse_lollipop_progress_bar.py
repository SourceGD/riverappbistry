from kivymd.uix.anchorlayout import MDAnchorLayout
from kivy.properties import NumericProperty, ColorProperty

from src.front.components.widget import ReverseLollipop

class ReverseLollipopProgressBar(MDAnchorLayout):
    """
        This class contains the code used to generate a progress bar
        using the reverse lollipop design.
    """
    progress_bar_size = NumericProperty(1)
    progress_bar_color = ColorProperty("#FFFFFF")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.display_progress_bar()

    def display_progress_bar(self) -> None:
        """
            Create and display the progress bar
        """
        self.clear_widgets()

        for i in range(self.progress_bar_size):
            self.add_widget(ReverseLollipop(order=i+1, lollipop_color=self.progress_bar_color))

    def on_progress_bar_size(self, *args) -> None:
        """ 
            Numeric property allows float and int but in this case we only want int value
        """
        self.display_progress_bar()

    def on_progress_bar_color(self, *args) -> None:
        self.display_progress_bar()

    def activate_lollipop(self, order: int) -> None :
        """
            Toggle the active attribute of lollipop children
        """
        if not isinstance(order, int):
            raise TypeError(f'order should be an int: {type(order)}')

        for child in self.children:
            if isinstance(child, ReverseLollipop):
                child.active = child.order >= order
