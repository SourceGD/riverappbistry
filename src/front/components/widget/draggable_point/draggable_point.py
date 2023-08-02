from kivymd.uix.widget import MDWidget

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