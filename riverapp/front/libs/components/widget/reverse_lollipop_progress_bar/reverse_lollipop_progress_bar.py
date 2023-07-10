from kivymd.uix.anchorlayout import MDAnchorLayout
from kivy.properties import NumericProperty

from libs.components.widget.reverse_lollipop.reverse_lollipop import ReverseLollipop

class ReverseLollipopProgressBar(MDAnchorLayout):
    progress_bar_size = NumericProperty(1)

    def __init__(self, *args, **kwargs) -> None:
        super(ReverseLollipopProgressBar, self).__init__(*args, **kwargs)
        self.display_progress_bar()

    def display_progress_bar(self) -> None:
        self.clear_widgets()

        for i in range(self.progress_bar_size):
            self.add_widget(ReverseLollipop(order=i+1))

    def on_progress_bar_size(self, instance, value) -> None:
        """ 
            Numeric property allows float and int but in this case we only want int value
        """
        if not isinstance(value, int):
            raise ValueError(f"progress_bar_size must be an int: {value}")

        self.display_progress_bar()
    
    def activate_lollipop(self, order: int) -> None :
        if not isinstance(order, int):
            raise TypeError(f'order should be an int: {type(order)}')
        
        for child in self.children:
            if isinstance(child, ReverseLollipop):
                child.active = (child.order==order)