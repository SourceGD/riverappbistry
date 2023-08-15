from kivymd.uix.relativelayout import MDRelativeLayout

from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, Line

from src.front.components.widget import DraggablePoint

class ShapeOnImage(MDRelativeLayout):
    def __init__(self, image:Image, coordinates: list = [], label_format: str ="", close_shape: bool = True, shape_width: int | float = 1, **kwargs):
        super().__init__(**kwargs)
        self.image = image
        self.coordinates: list = coordinates       
        self.label_format: str = label_format
        self.close_shape: bool = close_shape
        self.shape_width: int | float = shape_width
        self.shape: Line = None
        self.point_labels: list = []
        self.points: list = self._load_points()
        self.size_hint_x = None 
        
    def _load_points(self) -> list:
        if not self.coordinates:
            return []
        
        points: list = []
        for (x, y) in self.coordinates:
            fixed_xy = self._coordinate_fix(x,y)
            points.append(DraggablePoint(fixed_xy[0], fixed_xy[1]))
        
        return points
    
    def _coordinate_fix(self, x, y) -> tuple:
        fixed_x = x / self.image.norm_image_size[0] * self.width - 25
        fixed_y = y / self.image.norm_image_size[1] * self.height - 25

        if fixed_x < 0:
            fixed_x = 0
            
        elif fixed_x > self.width:
            fixed_x = self.width
            
        if fixed_y < 0 :
            fixed_y = 0
            
        elif fixed_y > self.height:
            fixed_y = self.height
            
        return (fixed_x, fixed_y)

    def get_points_center(self) -> list: 
        return [point.center for point in self.points]
    
    def draw_shape(self) -> None:
        self.point_labels = []
        self.shape = None
        self.clear_widgets()

        self.add_widget(self.image)
        
        # Drawing Shape within the canvas 
        with self.image.canvas:
            Color(1,0,1,1)
            self.shape = Line(points=self.get_points_center(), close=self.close_shape, width=self.shape_width)

        # Add DraggablePoint and its label to shape
        for i, point in enumerate(self.points):
            label_text = self.label_format + str(i + 1)

            # Update Shape when DraggablePoint position change
            point.bind(pos=self.update_shape)
            point.id = label_text
            self.add_widget(point)

            label = Label(text=label_text, color=(1,0,1,1))
            self.point_labels.append(label)
            self.add_widget(label)

            self.update_label_position(i)

    def update_label_position(self, index: int) -> None:
        # Place label next to point
        point = self.points[index]
        label = self.point_labels[index]
        label.pos = (point.x - 3.5 * point.width, point.y - 2 * point.height)

    def update_shape(self, *args) -> None:
        if self.shape is None:
            self.draw_shape()

        self.shape.points = self.get_points_center()

        # Update label position once the point mooved
        for i in range(len(self.points)):
            self.update_label_position(i)

    def on_touch_move(self, touch):
        for point in self.points:
            point.on_touch_move(touch)   
        
    def on_height(self, instance, value) -> None:
        self.width = self.height * self.image.image_ratio
        
        for i, point in enumerate(self.points):
            point.x, point.y = self._coordinate_fix(self.coordinates[i][0], self.coordinates[i][1]) 

        self.update_shape()

    def get_points_coordinate(self) -> list:
        coordinate: list = []

        for point in self.points:
            x = (point.x + 25) / self. width * self.image.norm_image_size[0]
            y = (point.y + 25) / self. height * self.image.norm_image_size[1]
            coordinate.append((x,y))

        return coordinate
    