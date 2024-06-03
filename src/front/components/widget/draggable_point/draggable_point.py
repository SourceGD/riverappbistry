from kivymd.uix.widget import MDWidget

class DraggablePoint(MDWidget):
    def __init__(self, x: float = 0, y: float = 0, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.size_hint = (None, None)
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

            self.pos = (new_x, new_y)

            return True
        
    def on_pos(self, instance, value) -> None :
        is_out_of_boundary, x, y = self.check_boundary(value[0], value[1])
        
        if is_out_of_boundary:
            self.pos = (x, y)

    def check_boundary(self, x: int | float, y: int | float) -> tuple:
        x_correction: float = x
        y_correction: float = y
        has_correction: bool = False

        if self.parent is not None:
            if x < self.parent.x - self.width / 2:
                x_correction = self.parent.x - self.width / 2
                has_correction = True

            elif x > self.parent.x + self.parent.width - self.width / 2:
                x_correction = self.parent.x + self.parent.width - self.width / 2
                has_correction = True

            if y < self.parent.y - self.parent.height:
                y_correction = self.parent.y - self.parent.height
                has_correction = True
                
            elif y > self.parent.y:
                y_correction = self.parent.y 
                has_correction = True
                
        return (has_correction, x_correction, y_correction)