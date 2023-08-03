from cv2 import VideoCapture, flip, CAP_PROP_POS_FRAMES, CAP_PROP_FPS
from os.path import exists
from matplotlib import pyplot as plt
from io import BytesIO
import numpy as np

from kivy.uix.image import Image
from kivy.graphics.texture import Texture


def video_to_image(video_path: str, time: int | float = 0) -> Image:
    
    if not isinstance(video_path, str):
        raise ValueError(f"video_path must be a string: {video_path}")
    
    if not exists(video_path):
        raise FileNotFoundError(f"Could not find {video_path}")
    
    if not isinstance(time, (float,int)):
        raise ValueError(f"time must be an int or a flaot: {time}")
    
    video_capture: VideoCapture = VideoCapture(video_path)
    
    if not video_capture.isOpened():
        raise IOError(f"Could not load {video_path}")
    
    video_capture.set(CAP_PROP_POS_FRAMES, int(time * video_capture.get(CAP_PROP_FPS)))
    
    success, frame = video_capture.read()
    
    video_capture.release()

    if not success:
        raise IOError(f"Could not read {video_path}")
    
    flipped_frame = flip(frame, 0)
    height, width, _ = flipped_frame.shape
    texture = Texture.create(size=(width, height))
    texture.blit_buffer(flipped_frame.tobytes(), colorfmt='bgr', bufferfmt='ubyte')

    return Image(texture=texture, size=(width, height), fit_mode="contain")


def plot_to_image(plot: plt) -> Image:
    image_buffer: BytesIO = BytesIO()
    
    plot.savefig(image_buffer, format="png")
    plot.close()
    image_buffer.seek(0)

    # Load image data from the BytesIO object
    image_data = plt.imread(image_buffer)
    height, width, _ = image_data.shape

    # Invert the image vertically
    image_data = np.flipud(image_data)

    # Convert the image into values from 0 to 255 (8 bits) 
    image_data = (image_data * 255).astype(np.uint8)

    # Create texture from image data
    texture = Texture.create(size=(width, height), colorfmt='rgba')
    texture.blit_buffer(image_data.flatten(), colorfmt='rgba', bufferfmt='ubyte')
    
    image_buffer.close()

    return Image(texture=texture, size=(width, height), fit_mode="contain")
    

    

    
