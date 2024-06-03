from kivymd.uix.widget import MDWidget

from kivymd.app import MDApp
from kivymd.uix.relativelayout import MDRelativeLayout

from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, Line

class DraggablePoint(MDWidget):
    def __init__(self, x: float = 0, y: float = 0, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.size = (50, 50) # Clickable area
        self.pos = (x - self.width / 2, y - self.height / 2 )

    def on_touch_down(self, touch) -> bool:
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True
        
    def on_touch_move(self, touch) -> bool:
        if touch.grab_current is self:
            new_x = touch.x - self.width / 2 
            new_y = touch.y - self.height / 2

            # Check if point is not out of parent
            if self.parent is not None and self.parent.parent is not None:

                if new_x < self.parent.x - self.width / 2:
                    new_x = self.parent.x - self.width / 2

                elif new_x > self.parent.x + self.parent.width - self.width / 2:
                    new_x = self.parent.x + self.parent.width - self.width / 2

                if new_y < self.parent.y - self.height / 2:
                    new_y = self.parent.y - self.height / 2

                elif new_y > self.parent.y + self.parent.height - self.height / 2:
                    new_y = self.parent.y + self.parent.height - self.height / 2

            self.pos = (new_x, new_y)
            return True
        
class ImageAreaSelection(Image):
    def __init__(self, source: str, **kwargs):
        super().__init__(**kwargs)

        self.source = source
        self.points = [
            DraggablePoint(0,0),
            DraggablePoint(0, self.height),
            DraggablePoint(self.width, self.height),
            DraggablePoint(self.width,0)
        ]
        self.label_string = "P"
        
        with self.canvas:
            # Create rectangle based off self.points position
            Color(1,0,1,1)
            self.rectangle = Line(points=self.get_rectangle_points(), close=True, width=2)

        for point in self.points:
            # Add draggable point into the picture
            self.add_widget(point)

            # Refresh rectangle when point position change 
            point.bind(pos=self.update_rectangle)

        # Create point label
        self.point_labels = []
        for i, point in enumerate(self.points):
            label_text = self.label_string + str(i + 1)
            label = Label(text=label_text, color=(1,0,1,1))
            self.point_labels.append(label)
            point.id = label_text

            self.add_widget(label)
            self.update_label_position(i)

    def update_rectangle(self, *args) -> None:
        self.rectangle.points = self.get_rectangle_points()

        # Update label position once the point mooved
        for i in range(len(self.points)):
            self.update_label_position(i)

    def get_rectangle_points(self) -> list: 
        return [point.center for point in self.points]
    
    def update_label_position(self, index: int) -> None:
        # Place label next to point
        point = self.points[index]
        label = self.point_labels[index]
        label.pos = (point.x - 0.6 * point.width, point.y - 0.05 * label.height)

    def on_touch_move(self, touch):
        for point in self.points:
            point.on_touch_move(touch)

class MainApp(MDApp):
    def build(self):
        root = MDRelativeLayout()
        root.adaptive_size = True
        root.md_bg_color='00ff00'
        root.pos = (100,100)
        root.add_widget(ImageAreaSelection(source='C:/Users/arnau/Desktop/riverapp/dev/utils/tag_vgc1.png'))
        
        return root


if __name__ == "__main__":
    MainApp().run()
