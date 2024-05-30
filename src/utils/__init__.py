"""
Init file for the image_generator and front-end utils module.
Video and Image Processing Utilities for Kivy Applications

This module provides functions for working with videos and converting them to Kivy Image objects.
It also offers a utility to convert matplotlib plots to Kivy Images.
It also offers a utility to check for an active internet connection.

Functions
---------

* `get_video_frame(video_path: str, time: int | float = 0) -> list`:
    - Retrieves a specific frame from a video using OpenCV.
    - Supports various video formats compatible with OpenCV.

* `video_to_image(video_path: str, time: int | float = 0) -> Image`:
    - Converts a video frame (obtained from `get_video_frame`) into a Kivy Image object.

* `plot_to_image(plot: plt) -> Image`:
    - Converts a matplotlib plot into a Kivy Image object.

* `check_internet() -> bool`:
    - Checks for an active internet connection.
"""
from .image_generator import video_to_image, plot_to_image, get_video_frame
from .utils import check_internet
