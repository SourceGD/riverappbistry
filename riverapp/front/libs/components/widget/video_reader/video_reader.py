from os import path 
import cv2

from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock

class VideoReader(Image):
    def __init__(self, video_path: str, fps: int=30, **kwargs):
        super().__init__(**kwargs)
        self.capture = cv2.VideoCapture(video_path)
        Clock.schedule_interval(self.update, 1.0/fps)

    def update(self, *args):
        ret, frame = self.capture.read()

        if ret:
            buffer = cv2.flip(frame, 0).tostring()
            image_texture = Texture.create(
                size= (frame.shape[1], frame.shape[0]), colorfmt='bgr'
            )
            image_texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')

            self.texture = image_texture