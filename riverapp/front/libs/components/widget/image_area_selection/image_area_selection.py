from os.path import exists

from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, Line

from libs.components.widget.draggable_point.draggable_point import DraggablePoint

class ImageAreaSelection(Image):
    def __init__(self, source: str, **kwargs):
        super().__init__(**kwargs)

        if not exists(source):
            raise FileNotFoundError(f"The file {source} was not founded")
         
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