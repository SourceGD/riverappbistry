import pytest
from os import path
from cv2 import VideoCapture, CAP_PROP_FPS, CAP_PROP_POS_FRAMES
from src.utils import get_video_frame, video_to_image, plot_to_image
import numpy as np

@pytest.fixture
def sample_video_path():
    return path.join(path.dirname(path.abspath(__file__)), "test_ressources/video.mp4")

def test_get_video_frame_invalid_video_path():
    with pytest.raises(ValueError):
        get_video_frame(55)

    with pytest.raises(FileNotFoundError):
        get_video_frame("invalid_video_path.mp4")

def test_get_video_frame_invalid_time(sample_video_path):
    with pytest.raises(ValueError):
        get_video_frame(sample_video_path, "invalid_time")

def test_get_video_frame_valid_input(sample_video_path):
    frame = get_video_frame(sample_video_path)
    assert isinstance(frame, list)

def test_get_video_frame_time(sample_video_path):
    time = 2.0
    frame = get_video_frame(sample_video_path, time)
    
    video_capture = VideoCapture(sample_video_path)
    expected_frame_num = int(time * video_capture.get(CAP_PROP_FPS))
    
    video_capture.set(CAP_PROP_POS_FRAMES, expected_frame_num)
    _, expected_frame = video_capture.read()
    video_capture.release()
    
    assert np.array_equal(frame, expected_frame)